# Qwen3-stagiaria 1.0

<img width="639" height="564" alt="Screenshot 2025-08-22 at 8 51 57 AM" src="https://github.com/user-attachments/assets/5c11a648-d148-4fe8-a099-a63df2180177" />


## 📁 Conteúdo do Repositório

```
Qwen3-estagiaria/
├── 📄 README.md                    # Documentação do projeto
├── 🐍 mac_stagiaria.py             # Versão para Mac/Linux
├── 🐍 windows_stagiaria.py         # Versão para Windows
├── 📄 .env                         # Variáveis de ambiente
├── 📄 custom_qwen.modelfile        # Configuração personalizada do modelo Qwen
├── 📄 custom_granite.modelfile     # Configuração personalizada do modelo Granite
├── 📄 custom_qwen_mini.modelfile   # Configuração personalizada do modelo Qwen Mini
├── 📄 LICENSE                      # Licença do projeto
├── 📁 development/                 # Código de desenvolvimento e testes
│   ├── 🐍 ia_stagiaria_image.py    # Versão de desenvolvimento com suporte a imagens
│   └── 📄 Ollama Terminal settings.TXT
├── 📁 sample_documents/            # Arquivos de exemplo para testes
│   ├── 📁 inputs/                  # Arquivos de entrada de exemplo
│   │   ├── 📄 test_paper.pdf       # PDF de exemplo
│   │   └── 🖼️ poverty infographics.jpg  # Imagem de exemplo
│   └── 📁 outputs/                 # Diretório para resultados dos testes
└── 📄 imagen_1.png                 # Imagem de exemplo
```

## Ferramenta de Processamento de Textos Privados

Esta é uma ferramenta que permite fazer o processamento de textos privados ou que devem permanecer com sigilo, já que tudo é processado unicamente na máquina do usuário. Aqui nenhum documento sensível é enviado para as IA na nuvem tipo OpenAI com o ChatGPT ou o Google com o Gemini. Aqui é privacidade ante tudo.

### Recursos

- Interface gráfica para uso fácil
- Seleção de diretório de entrada (contendo arquivos PDF/Word/Imagens)
- Seleção de diretório de saída
- Texto do prompt personalizável
- Conversão automática de PDF para texto usando PyPDF2
- Conversão automática de documentos Word para texto usando python-docx
- **Processamento multimodal com suporte a imagens** (JPEG, JPG, PNG, TIFF)
- Integração com LLM Ollama para processamento
- Cria arquivos "_source.txt" para cada documento de entrada
- Gera arquivos "_ficha.txt" com resultados processados pelo LLM

### Privacidade e Segurança

- **Processamento Local Total**: Todos os arquivos são processados localmente na sua máquina
- **Nenhuma Dados na Nuvem**: Nenhum documento sensível é enviado para serviços de IA na nuvem
- **Confidencialidade Garantida**: Seus textos privados permanecem em sua máquina durante todo o processo
- **Privacidade Ante Tudo**: Esta ferramenta foi desenvolvida com foco exclusivo na privacidade do usuário

### Requisitos

#### Dependências Python
- Python 3.6+ (instalado no computador, ou ainda melhor, num environment de conda)
- PyPDF2 (`conda install -c conda-forge pypdf2` ou `pip install pypdf2`)
- python-docx (`conda install -c conda-forge python-docx` ou `pip install python-docx`)

#### Configuração do Ollama
Esta aplicação requer que o Ollama esteja instalado e em execução na sua máquina. A aplicação usa especificamente o modelo `qwen3-4b-16k`. Você pode baixar o Ollama em: [https://ollama.com/download](https://ollama.com/download)

#### Instalação do Modelo
Antes de usar esta aplicação, você deve ter o modelo necessário do Ollama instalado. Execute o seguinte comando em seu terminal:

Se seu computador tem menos de 3 anos (RECOMENDADO)

```bash
ollama pull hf.co/unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M
```

Se voce voce tem um computador "vintage":
```bash
ollama pull granite3.3:2b
```

Se você quiser usar uma configuração de modelo personalizada, pode criar uma usando o arquivo modelfile fornecido:

de novo, para computadores relativamente novos (RECOMENDADO)
```bash
ollama create MyModel -f custom_qwen.modelfile
```

Ou para computadores vintage:
```bash
ollama create MyModel -f custom_granite.modelfile
```

### Uso

1. No Windows: Execute a aplicação GUI:
   ```
   python3 windows_stagiaria.py
   ```
   Ou asism se voce usa um environment de conda:
   ```
   python windows_stagiaria.py
   ```

   No Mac/Linux: Execute a aplicação GUI:
   ```
   python3 mac_stagiaria.py
   ```
   Ou asism se voce usa um environment de conda:
   ```
   python mac_stagiaria.py
   ```

2. Na GUI:
   - Selecione o diretório de entrada contendo arquivos PDF/Word/Imagens/texto
   - Selecione o diretório de saída onde os resultados serão salvos
   - Modifique o texto do prompt se necessário (o padrão já está preenchido)
   - Clique em "Processar Arquivos"

3. A aplicação irá:
   - Converter documentos PDF e Word em arquivos de texto
   - Coletar arquivos de imagem para processamento multimodal
   - Processar todos os arquivos (texto + imagens) com o LLM usando seu prompt
   - Salvar os resultados em um subdiretório "fichas" do diretório de saída

### Estrutura de Arquivos

- Arquivos de entrada (PDF/Word/Imagens/texto) são processados:
  - PDF e Word são convertidos para o formato `_source.txt`
  - Imagens são coletadas para processamento multimodal direto com o LLM
- Resultados do LLM são salvos em um subdiretório `fichas` como `combined_ficha.txt` (processamento combinado de todos os arquivos)

### Exemplo de Saída

Para um arquivo de entrada `artigo.pdf`, o processo cria:
- `artigo_source.txt` (convertido do PDF)
- `artigo_ficha.txt` (resultado processado pelo LLM em formato de ficha)

### Notas

- A aplicação criará automaticamente os diretórios necessários
- A conversão de PDF e Word requer as respectivas bibliotecas estarem instaladas
- O processamento com LLM usa o modelo `qwen2.5vl:latest` via Ollama para suporte multimodal
- **Novidade**: Agora suporta processamento direto de imagens (JPEG, JPG, PNG, TIFF) junto com documentos de texto
- Todas as imagens e textos são processados em conjunto para gerar um resumo combinado

### Créditos

Desenvolvida por Jorge Leon Sarmiento & Qwen-Coder

<img width="219" height="404" alt="Qwen-stagiaria" src="https://github.com/user-attachments/assets/ce6aebf3-93b4-4c3f-8204-5ce993098d90" />
