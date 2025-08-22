# Qwen3-stagiaria 1.0

<img width="639" height="564" alt="Screenshot 2025-08-22 at 8 51 57 AM" src="https://github.com/user-attachments/assets/5c11a648-d148-4fe8-a099-a63df2180177" />


Uma interface gráfica baseada em tkinter que envolve o script existente `process_texts.py` com funcionalidades aprimoradas para processar documentos PDF e Word.

## Recursos

- Interface gráfica para uso fácil
- Seleção de diretório de entrada (contendo arquivos PDF/Word)
- Seleção de diretório de saída
- Texto do prompt personalizável
- Conversão automática de PDF para texto usando PyPDF2
- Conversão automática de documentos Word para texto usando python-docx
- Integração com LLM Ollama para processamento
- Cria arquivos "_source.txt" para cada documento de entrada
- Gera arquivos "_ficha.txt" com resultados processados pelo LLM

## Requisitos

### Dependências Python
- Python 3.6+
- PyPDF2 (`conda install -c conda-forge pypdf2`)
- python-docx (`conda install -c conda-forge python-docx`)

### Configuração do Ollama
Esta aplicação requer que o Ollama esteja instalado e em execução na sua máquina. A aplicação usa especificamente o modelo `qwen3-4b-32k`.

### Instalação do Modelo
Antes de usar esta aplicação, você deve ter o modelo necessário do Ollama instalado. Execute o seguinte comando em seu terminal:

```bash
ollama pull hf.co/unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M
```

Se você quiser usar uma configuração de modelo personalizada, pode criar uma usando o arquivo modelfile fornecido:

```bash
ollama create qwen3-4b-32k -f qwen3-4b-32k.modelfile
```

## Uso

1. Execute a aplicação GUI:
   ```
   python3 text_processor_gui.py
   ```

2. Na GUI:
   - Selecione o diretório de entrada contendo arquivos PDF/Word/texto
   - Selecione o diretório de saída onde os resultados serão salvos
   - Modifique o texto do prompt se necessário (o padrão já está preenchido)
   - Clique em "Processar Arquivos"

3. A aplicação irá:
   - Converter documentos PDF e Word em arquivos de texto
   - Processar cada arquivo de texto com o LLM usando seu prompt
   - Salvar os resultados em um subdiretório "fichas" do diretório de saída

## Estrutura de Arquivos

- Arquivos de entrada (PDF/Word/texto) são processados e convertidos para o formato `_source.txt`
- Resultados do LLM são salvos em um subdiretório `fichas` como `_ficha.txt`

## Exemplo de Saída

Para um arquivo de entrada `artigo.pdf`, o processo cria:
- `artigo_source.txt` (convertido do PDF)
- `artigo_ficha.txt` (resultado processado pelo LLM em formato de ficha)

## Notas

- A aplicação criará automaticamente os diretórios necessários
- A conversão de PDF e Word requer as respectivas bibliotecas estarem instaladas
- O processamento com LLM usa o modelo `qwen3-4b-32k:latest` do Ollama
- Certifique-se de que o Ollama esteja em execução em modo serve antes de iniciar a aplicação

## Créditos

Desenvolvida por Jorge Leon Sarmiento & Qwen-Coder
