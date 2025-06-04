# 🧑‍💻 **Projeto de Processamento de Dados Tabulares via API**

Este projeto demonstra como criar uma API em **FastAPI** para receber arquivos CSV, processar dados tabulares com **pandas** e retornar estatísticas agregadas (soma, média e contagem), tanto no geral quanto por categoria. Inclui containerização com **Docker** e um **Jupyter Notebook** que exemplifica o consumo do endpoint de forma prática.

---

## 🎯 **Objetivo**
- Construir um endpoint `/upload-csv` capaz de receber CSVs via multipart/form-data e gerar respostas em JSON com estatísticas agregadas.
- Mostrar, em um **notebook interativo**, como consumir a API, carregar o CSV e visualizar os resultados em DataFrames e gráficos simples.

---

## 🛠 **Tecnologias e Ferramentas Usadas**
- **Linguagem:** Python
- **Framework de API:** FastAPI
- **Bibliotecas:**
  - `pandas`: Leitura e processamento de dados tabulares
  - `FastAPI`: Criação de rotas REST e tratamento de uploads
  - `uvicorn[standard]`: Servidor ASGI para executar a aplicação
  - `python-multipart`: Suporte ao upload de arquivos via FastAPI
  - `requests`: Requisições HTTP no notebook de exemplo
  - `matplotlib`: Visualização de gráficos no Jupyter Notebook
- **Containerização:** Docker
- **Ambiente Interativo:** Jupyter Notebook

---

## 📂 **Estrutura do Projeto**
    .
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   └── data/
    │       └── sample_data.csv
    │
    ├── notebooks/
    │   └── tabular_api_example.ipynb
    │
    ├── requirements.txt
    ├── Dockerfile
    └── README.md

- **app/main.py**: Contém a lógica do FastAPI, com o endpoint `/upload-csv` que lê o CSV, calcula estatísticas (total, média, contagem) e agrupa por categoria.  
- **app/data/sample_data.csv**: CSV de exemplo com colunas `id`, `data`, `categoria` e `valor`, usado para testar o endpoint.  
- **notebooks/tabular_api_example.ipynb**: Notebook que demonstra o uso da API: carrega o CSV local, faz requisição ao endpoint e exibe DataFrames e gráficos.  
- **requirements.txt**: Lista todas as dependências do Python necessárias, incluindo FastAPI, pandas e uvicorn.  
- **Dockerfile**: Define a imagem Docker para rodar a aplicação, instalando dependências e expondo a porta 8000.  
- **README.md**: Documentação deste repositório.

---

## 🧠 **Métodos Implementados**
- **Endpoint `/upload-csv`**  
  - Recebe um arquivo CSV via `UploadFile`  
  - Valida se o arquivo termina com `.csv`  
  - Lê o conteúdo em um DataFrame pandas  
  - Verifica a presença das colunas `categoria` e `valor`  
  - Calcula:
    - `total_geral`: soma de todos os valores  
    - `media_geral`: média de todos os valores  
    - `contagem_geral`: número total de registros  
  - Agrupa por `categoria` e retorna soma, média e contagem para cada grupo  
  - Retorna um JSON com as estatísticas no formato:
        {
          "total_geral": float,
          "media_geral": float,
          "contagem_geral": int,
          "agregados_por_categoria": [
            { "categoria": "A", "sum": float, "mean": float, "count": int },
            ...
          ]
        }

- **Notebook de Exemplo**  
  - Mostra como instalar dependências (caso rode fora de Docker)  
  - Carrega `sample_data.csv` em um DataFrame  
  - Envia o arquivo para a rota `/upload-csv` usando `requests`  
  - Converte o JSON de resposta em DataFrames pandas  
  - Exibe as estatísticas gerais e por categoria  
  - Gera um gráfico de barras ilustrando a soma por categoria

---

## 📊 **Resultados Obtidos**
Ao enviar o CSV de exemplo, a API retorna corretamente os seguintes valores:
    {
      "total_geral": 1691.6,
      "media_geral": 169.16,
      "contagem_geral": 10,
      "agregados_por_categoria": [
        { "categoria": "A", "sum": 365.5, "mean": 91.375, "count": 4 },
        { "categoria": "B", "sum": 405.75, "mean": 135.25, "count": 3 },
        { "categoria": "C", "sum": 700.25, "mean": 350.125, "count": 2 },
        { "categoria": "D", "sum": 220.1, "mean": 220.1, "count": 1 }
      ]
    }
Esses valores conferem com o cálculo manual dos dados em `sample_data.csv`. O notebook ilustra a visualização gráfica desses resultados, facilitando a interpretação.

---

## 📷 **Exemplo de Uso**
1. **Rodando o container Docker**  
       docker build -t tabular-api .  
       docker run -d --name tabular-api -p 8000:8000 tabular-api  

2. **Acessando o Swagger UI**  
   No navegador, abra:  
       http://localhost:8000/docs  
   e teste o envio de um arquivo CSV diretamente pela interface.

3. **Notebook de Demonstração**  
   Abra o Jupyter Notebook em `notebooks/tabular_api_example.ipynb` e execute as células para:  
   - Carregar `sample_data.csv`  
   - Fazer requisição ao endpoint `/upload-csv`  
   - Exibir DataFrames e gráfico de barras da soma por categoria

---

## 🚀 **Próximos Passos**
- **Validação mais robusta**: Implementar checagens de esquema (schema validation) para garantir que o CSV contenha colunas adicionais ou tipos de dados esperados.  
- **Pipelines de CI/CD**: Configurar GitHub Actions para executar testes automatizados e build Docker a cada commit.  
- **Adição de modelo preditivo**: Incorporar um endpoint extra que faça previsões simples usando scikit-learn sobre os dados enviados.  
- **Interface Web**: Criar um frontend em React ou Streamlit que permita arrastar e soltar o CSV e visualizar os gráficos dinamicamente.  
- **Configuração de HTTPS**: Adicionar um proxy reverso (nginx ou Traefik) para servir a API com certificado Let’s Encrypt.

---

## 👤 **Autor**
Guilherme Koiti Tanaka Sassaki  
[LinkedIn](https://www.linkedin.com/in/guilherme-sassaki-10b81ba7/)  
