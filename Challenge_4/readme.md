# Challenge 4 - Relatório VR Mensal com IA Agents

Este projeto implementa um sistema de IA que gera automaticamente relatórios de Vale Refeição (VR) mensal para colaboradores admitidos em abril, utilizando agentes inteligentes para processar e filtrar dados de RH.

## 📋 Descrição do Projeto

O sistema processa dados de admissões, estagiários e afastamentos para gerar um relatório Excel.

## 🛠️ Pré-requisitos

### Dependências do Sistema
- **Python 3.11+**
- **pip** (gerenciador de pacotes Python)

### API Keys Necessárias
- **Google Gemini API Key** - Para o modelo de linguagem

## ⚙️ Configuração

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd Challenge_4
```

### 2. Instalar Dependências Python
Instale todas as dependências necessárias usando o arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
Copie o arquivo de exemplo e configure suas API keys:
```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
GOOGLE_API_KEY=sua_google_gemini_api_key_aqui
```

### 4. Preparar Dados de Entrada
Coloque os arquivos Excel na pasta `input_data/`:
- `ADMISSÃO ABRIL.xlsx` - Dados de admissões de abril
- `ESTÁGIO.xlsx` - Lista de estagiários  
- `AFASTAMENTOS.xlsx` - Lista de afastamentos
- Outros arquivos conforme necessário

## 🚀 Como Executar

### Execução Única
```bash
python main.py
```

Este comando executa automaticamente:
1. **Carregamento dos dados** - Lê os arquivos Excel da pasta `input_data/`
2. **Processamento com IA** - Executa o agente para filtrar e processar os dados
3. **Geração do relatório** - Cria a planilha Excel final na pasta `output/`

> **Nota**: Não é necessário executar `ingest_data.py` separadamente, pois o carregamento dos dados é feito automaticamente pelo `main.py`.
## 📁 Estrutura do Projeto

```
Challenge_4/
├── ai_agent/                      # Módulo principal dos agentes
│   ├── agent_config.py           # Configuração dos agentes
│   ├── agent_process.py          # Lógica de processamento principal
│   └── tools/                    # Ferramentas do agente
│       ├── processment.py        # Tools de consulta aos dados
│       └── utils.py              # Tools de manipulação/exportação
├── singletons/                   # Gerenciamento de dados
│   └── dataframes.py            # Singleton dos DataFrames
├── input_data/                   # Dados de entrada (Excel)
├── output/                       # Relatórios gerados
├── ingest_data.py               # Script de carregamento de dados
├── main.py                      # Script principal
├── requirements.txt             # Dependências Python
├── .env                         # Variáveis de ambiente
├── .env.example                 # Exemplo de configuração
└── README.md                    # Esta documentação
```

## 🔧 Componentes Principais

### Agent Process
- **VRMensalChain**: Chain estruturada para processamento sequencial
- **VRMensalChainFallback**: Método de fallback usando prompt único
- **Steps**: Consulta admissões → Consulta estagiários → Consulta afastamentos → Processamento → Geração de planilha

### Tools Disponíveis

#### Tools de Consulta (`processment.py`)
- `consultar_admissao_abril` - Consulta colaboradores admitidos em abril com datas
- `consultar_estagio` - Consulta lista completa de estagiários
- `consultar_afastamentos` - Consulta colaboradores com status de afastamento
- `consultar_aprendiz` - Consulta lista de aprendizes
- `consultar_ativos` - Consulta colaboradores ativos
- `consultar_desligados` - Consulta colaboradores desligados
- `consultar_exterior` - Consulta colaboradores no exterior
- `consultar_ferias` - Consulta colaboradores em férias
- `consultar_vr_mensal` - Consulta dados do vale refeição mensal
- `consultar_base_dias_uteis` - Consulta base de dias úteis
- `consultar_base_sindicato_valor` - Consulta valores por sindicato

#### Tools de Manipulação (`utils.py`)
- `gerar_planilha_excel` - Gera planilha Excel a partir de dados CSV
- `response_to_df` - Converte resposta de texto em DataFrame
- `df_to_excel` - Exporta DataFrame para arquivo Excel
- `df_to_csv` - Exporta DataFrame para arquivo CSV

### Singleton DataFrames
Gerencia os DataFrames carregados em memória para acesso eficiente em tempo de execução.

## 📊 Saída Esperada

O sistema gera:
1. **Planilha Excel**: `output/relatorio_vr_mensal_abril_YYYYMMDD_HHMMSS.xlsx`
2. **CSV**: `output/relatorio_vr_mensal_abril.csv`

## 🚨 Solução de Problemas

### Erro de Dependências
```
ModuleNotFoundError: No module named 'pandas'
```
**Solução**: Execute `pip install -r requirements.txt`

### Erro de API Key
```
Error: Google API key not found
```
**Solução**: Verifique se `GOOGLE_API_KEY` está configurada no `.env`

### Erro de Dados Não Encontrados
```
Error: DataFrame not found
```
**Solução**: Execute `python ingest_data.py` primeiro

### Planilha Não Gerada
- Verifique se a pasta `output/` existe
- Verifique permissões de escrita
- Execute novamente com logs habilitados

### Conflitos de Versão
Se houver conflitos de dependências:
```bash
pip install --upgrade -r requirements.txt
```