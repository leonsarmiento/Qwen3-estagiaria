#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
from pathlib import Path

# Try to import PDF and Word parsing libraries
try:
    import PyPDF2
    pdf_support = True
except ImportError:
    pdf_support = False

try:
    from docx import Document
    word_support = True
except ImportError:
    word_support = False

class TextProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Qwen3-stagiaria 1.0 - PDF/Word to Text Converter")
        self.root.geometry("600x500")
        
        # Default prompt text from the original script
        self.default_prompt = "VOCE É UM REVISOR DE BIBLIOGRAFIA QUE PROCESSA TEXTOS CIENTÍFICOS EN INGLÉS E CRIE FICHAS BIBLIOGRÁFICAS EM PORTUGES. Tarefa: Leia o texto seguinte e crie um documento de resumo após ler cada um com as seguintes informações em português: Título; Autores; DOI (se houver); Citação conforme ABNT; Objetivo do artigo; Principais resultados e conclusões; Referência utilizada mais importante (se houver); LEMBRE-SE: EM PORTUGUÊS."
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input directory selection
        ttk.Label(main_frame, text="Input Directory (with PDF/Word files):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_dir_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_dir_var, width=50)
        input_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_input_dir)
        input_browse_btn.grid(row=1, column=2, sticky=tk.W, pady=5, padx=(5,0))
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(main_frame, textvariable=self.output_dir_var, width=50)
        output_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_output_dir)
        output_browse_btn.grid(row=3, column=2, sticky=tk.W, pady=5, padx=(5,0))
        
        # Prompt text
        ttk.Label(main_frame, text="Prompt Text:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.prompt_text_var = tk.StringVar(value=self.default_prompt)
        prompt_textbox = tk.Text(main_frame, height=6, width=60)
        prompt_textbox.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        prompt_textbox.insert(tk.END, self.default_prompt)
        
        # Process button
        self.process_btn = ttk.Button(main_frame, text="Process Files", command=self.start_processing)
        self.process_btn.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=8, column=0, columnspan=3, pady=5)
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(5, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Check if required libraries are available
        self.check_dependencies()
        
    def check_dependencies(self):
        """Check if required libraries are available for PDF/Word parsing"""
        missing_libs = []
        if not pdf_support:
            missing_libs.append("PyPDF2")
        if not word_support:
            missing_libs.append("python-docx")
            
        if missing_libs:
            messagebox.showwarning(
                "Missing Dependencies",
                f"Following libraries are not installed for PDF/Word parsing:\n{', '.join(missing_libs)}\n\n"
                "To enable PDF/Word support, please install them using:\npip install PyPDF2 python-docx"
            )
    
    def browse_input_dir(self):
        """Open dialog to select input directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir_var.set(directory)
    
    def browse_output_dir(self):
        """Open dialog to select output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
    
    def start_processing(self):
        """Start processing in a separate thread"""
        # Validate inputs
        input_dir = self.input_dir_var.get().strip()
        output_dir = self.output_dir_var.get().strip()
        prompt_text = self.prompt_text_var.get().strip()
        
        if not input_dir:
            messagebox.showerror("Error", "Please select an input directory")
            return
            
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        if not os.path.exists(input_dir):
            messagebox.showerror("Error", "Input directory does not exist")
            return
            
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output directory: {e}")
                return
                
        # Start processing in a separate thread
        self.process_btn.config(state='disabled')
        self.progress.start()
        self.status_var.set("Processing files...")
        
        thread = threading.Thread(
            target=self.process_files,
            args=(input_dir, output_dir, prompt_text)
        )
        thread.daemon = True
        thread.start()
    
    def process_files(self, input_dir, output_dir, prompt_text):
        """Process all files in the input directory"""
        try:
            # Create a temporary directory for processed text files
            temp_dir = os.path.join(output_dir, "temp_processed")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Get all files in input directory
            files = [f for f in os.listdir(input_dir) 
                    if os.path.isfile(os.path.join(input_dir, f))]
            
            total_files = len(files)
            processed_count = 0
            
            # Process each file
            for filename in files:
                file_path = os.path.join(input_dir, filename)
                self.status_var.set(f"Processing {filename}...")
                
                # Determine file type and process accordingly
                if filename.lower().endswith('.pdf'):
                    if pdf_support:
                        self.process_pdf_file(file_path, temp_dir, filename)
                    else:
                        self.status_var.set(f"Skipping {filename} - PDF support not available")
                        continue
                        
                elif filename.lower().endswith(('.doc', '.docx')):
                    if word_support:
                        self.process_word_file(file_path, temp_dir, filename)
                    else:
                        self.status_var.set(f"Skipping {filename} - Word support not available")
                        continue
                        
                else:
                    # Assume it's already a text file
                    self.copy_text_file(file_path, temp_dir, filename)
                
                processed_count += 1
                self.update_progress(processed_count, total_files)
            
            # Now process all the text files with LLM
            self.process_text_files_with_llm(temp_dir, output_dir, prompt_text)
            
            # Cleanup temp directory
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            self.status_var.set("Processing complete!")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Processing failed: {e}")
        finally:
            self.progress.stop()
            self.process_btn.config(state='normal')
    
    def process_pdf_file(self, file_path, output_dir, original_filename):
        """Extract text from PDF and save as .txt"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                # Save as text file with "_source.txt" suffix
                output_filename = os.path.splitext(original_filename)[0] + "_source.txt"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    
        except Exception as e:
            raise Exception(f"Error processing PDF {original_filename}: {e}")
    
    def process_word_file(self, file_path, output_dir, original_filename):
        """Extract text from Word document and save as .txt"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # Save as text file with "_source.txt" suffix
            output_filename = os.path.splitext(original_filename)[0] + "_source.txt"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
                
        except Exception as e:
            raise Exception(f"Error processing Word document {original_filename}: {e}")
    
    def copy_text_file(self, file_path, output_dir, original_filename):
        """Copy text file as is with proper encoding handling"""
        try:
            # Save as text file with "_source.txt" suffix
            output_filename = os.path.splitext(original_filename)[0] + "_source.txt"
            output_path = os.path.join(output_dir, output_filename)
            
            # Try to read the file with different encodings
            content = None
            encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings_to_try:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break  # Success, exit the loop
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    raise Exception(f"Error reading text file {original_filename}: {e}")
            
            if content is None:
                # If all encodings failed, try with error handling
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
            # Write with UTF-8 encoding
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            raise Exception(f"Error processing text file {original_filename}: {e}")
    
    def process_text_files_with_llm(self, input_dir, output_dir, prompt_text):
        """Process text files with LLM using the original script logic"""
        try:
            # Create fichas directory if it doesn't exist
            fichas_dir = os.path.join(output_dir, "fichas")
            os.makedirs(fichas_dir, exist_ok=True)
            
            # Process each text file in the input directory
            for filename in os.listdir(input_dir):
                if filename.endswith("_source.txt"):
                    # Create full paths
                    input_path = os.path.join(input_dir, filename)
                    output_filename = filename.replace("_source.txt", "_ficha.txt")
                    output_path = os.path.join(fichas_dir, output_filename)
                    
                    self.status_var.set(f"Processing {filename} with LLM...")
                    
                    try:
                        # Read the content of the input file
                        with open(input_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        
                        # Create the command with proper escaping
                        cmd = ['ollama', 'run', 'MyModel:latest', prompt_text]
                        
                        # Set environment variables for proper Unicode handling on Windows
                        env = os.environ.copy()
                        env['PYTHONIOENCODING'] = 'utf-8'
                        
                        # Execute the command with the file content as stdin
                        # Explicitly set encoding for Windows compatibility
                        result = subprocess.run(
                            cmd,
                            input=file_content,
                            text=True,
                            encoding='utf-8',
                            capture_output=True,
                            check=True,
                            env=env
                        )
                        
                        # Ensure the output is properly encoded before writing
                        output_content = result.stdout
                        
                        # Write the output to the fichas directory with error handling
                        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
                            f.write(output_content)
                        
                    except subprocess.CalledProcessError as e:
                        if "failed to connect" in str(e.stderr).lower() or "connection refused" in str(e.stderr).lower():
                            raise Exception("Ollama is not running or not accessible. Please start Ollama server.")
                        raise Exception(f"Error processing {filename}: {e}")
                    except UnicodeEncodeError as ue:
                        # Handle specific encoding errors
                        raise Exception(f"Encoding error processing {filename}: {ue}. The content may contain unsupported characters.")
                    except Exception as e:
                        raise Exception(f"Unexpected error processing {filename}: {e}")
                        
        except Exception as e:
            raise Exception(f"Error in LLM processing: {e}")
    
    def update_progress(self, current, total):
        """Update progress bar"""
        # This is a simple placeholder - in a real implementation,
        # we would update the progress bar with actual values
        pass

def main():
    root = tk.Tk()
    app = TextProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
