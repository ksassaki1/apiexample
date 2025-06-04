from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io

app = FastAPI()

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    # Verifica se o conteúdo é CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Envie um arquivo CSV")
    try:
        # Lê o conteúdo do arquivo em memória e carrega no pandas
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler CSV: {e}")

    # Supondo que o CSV tenha colunas: 'categoria' e 'valor'
    if "categoria" not in df.columns or "valor" not in df.columns:
        return JSONResponse(
            status_code=200,
            content={"detail": "O CSV deve ter colunas 'categoria' e 'valor'."}
        )

    # Exemplo de estatísticas agregadas
    total_geral = df["valor"].sum()
    media_geral = df["valor"].mean()
    count_geral = df["valor"].count()

    # Estatísticas por categoria
    agregados_por_categoria = (
        df.groupby("categoria")["valor"]
        .agg(["sum", "mean", "count"])
        .reset_index()
        .to_dict(orient="records")
    )

    retorno = {
        "total_geral": float(total_geral),
        "media_geral": float(media_geral),
        "contagem_geral": int(count_geral),
        "agregados_por_categoria": agregados_por_categoria
    }
    return JSONResponse(status_code=200, content=retorno)
