# 🧑‍💻 Processamento de Dados Tabulares — API FastAPI + PostgreSQL

Este repositório demonstra como criar uma API **FastAPI** que  

1. recebe arquivos CSV via `multipart/form-data`;  
2. grava o conteúdo em **PostgreSQL** (ou MongoDB, se `BACKEND=mongo`);  
3. devolve estatísticas agregadas (soma, média e contagem) em JSON, tanto gerais quanto por categoria.

Tudo já vem conteinerizado com **Docker Compose** e acompanhado de um **Jupyter Notebook** que exemplifica o consumo do endpoint.

---

## 🎯 Objetivos

* **Endpoint `/v1/upload-csv`**  
  * valida as colunas obrigatórias (`categoria`, `valor`);  
  * persiste os dados no banco;  
  * devolve as estatísticas agregadas geradas em *pandas*.  

* **Arquitetura modular** – configuração, ingestão, persistência e rota em módulos separados.  

* **Exemplo interativo** – o notebook `notebooks/ex.ipynb` mostra como enviar o CSV e visualizar o retorno.

---

## 🛠 Tecnologias

| Camada            | Ferramentas principais                                                 |
|-------------------|------------------------------------------------------------------------|
| **API**           | FastAPI · Uvicorn · Pydantic (`pydantic-settings`)                     |
| **Processamento** | pandas                                                                 |
| **Persistência**  | **PostgreSQL + SQLAlchemy (assíncrono)**  (opcional → MongoDB + Motor) |
| **Infra**         | Docker · Docker Compose                                               |
| **Interativo**    | Jupyter Notebook · matplotlib                                          |

---

## 📂 Estrutura do projeto

```text
.
├── app
│   ├── api
│   │   └── v1
│   │       └── routes_upload.py      # rota /v1/upload-csv
│   ├── core
│   │   ├── config.py                 # carrega variáveis (.env)
│   │   └── db.py                     # engine Postgres / client Mongo
│   ├── data
│   │   └── sample_data.csv
│   ├── models
│   │   └── record.py                 # esquema Pydantic (opcional)
│   ├── services
│   │   ├── csv_loader.py             # leitura/validação do CSV
│   │   └── persistence.py            # grava DataFrame no banco
│   ├── main.py                       # instancia FastAPI e inclui rotas
│   └── __init__.py
├── docker-compose.yml                # Postgres + API
├── Dockerfile                        # imagem da aplicação
├── notebooks
│   └── ex.ipynb                      # demonstração de uso
├── requirements.txt
└── README.md
```

## ✈️ Subindo tudo com Docker Compose

# Clone o repositório
* git clone https://github.com/ksassaki1/tabular-api.git
* cd tabular-api

# Crie o arquivo .env com backend e string de conexão
BACKEND=postgres

POSTGRES_URI=postgresql+asyncpg://user:pass@db:5432/tabular_api


# Construa e rode os containers
docker compose up -d --build

A stack levanta dois serviços:

    db → Postgres 16 (db:5432 dentro da rede)

    api → FastAPI em http://localhost:8001


## 🚀 Usando a API


1 · Swagger UI

Acesse http://localhost:8001/docs e faça upload de app/data/sample_data.csv.

2 · cURL

curl -F "file=@app/data/sample_data.csv" \
     http://localhost:8001/v1/upload-csv

Resposta típica:

```

{
  "total_geral": 1691.6,
  "media_geral": 169.16,
  "contagem_geral": 10,
  "agregados_por_categoria": [
    {"categoria": "A", "sum": 365.5, "mean": 91.375, "count": 4},
    {"categoria": "B", "sum": 405.75, "mean": 135.25, "count": 3},
    {"categoria": "C", "sum": 700.25, "mean": 350.125, "count": 2},
    {"categoria": "D", "sum": 220.1,  "mean": 220.1,   "count": 1}
  ]
}

```

3 · Notebook

Execute notebooks/ex.ipynb para:

    1-carregar o CSV de exemplo;

    2-enviá-lo ao endpoint;

    3-transformar o JSON em DataFrames;

    4-plotar a soma por categoria.

## 📝 Requisitos (pip)

*fastapi>=0.111
*uvicorn[standard]>=0.29
*pandas>=2.2
*python-multipart>=0.0.9
*SQLAlchemy>=2.0
*asyncpg>=0.29
*pydantic-settings>=2.1
*matplotlib>=3.9
# opcional para MongoDB
*motor>=3.4


## 🔮 Próximos passos

**Validação de esquema** – pandera ou Great Expectations.

**Autenticação** – OAuth2 + JWT e rate-limiting.

**CI/CD** – GitHub Actions rodando testes e build da imagem.

**Uploads grandes** – leitura em chunks de 50 k linhas.

**Frontend em Streamlit** - para drag-and-drop e visualização dinâmica.

**HTTPS** – Nginx + Let’s Encrypt como proxy reverso.

## 👤 Autor

Guilherme Koiti Tanaka Sassaki
[LinkedIn](https://www.linkedin.com/in/guilherme-sassaki-10b81ba7/)  
