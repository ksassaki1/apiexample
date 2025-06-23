# app/api/v1/routes_upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
import io
from app.services.csv_loader import csv_to_dataframe          # ajuste de import se o path for diferente
from app.services.persistence import persist_dataframe        # idem

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Envie um arquivo CSV")

    # carrega CSV → DataFrame
    try:
        df = await csv_to_dataframe(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # valida colunas mínimas
    if not {"categoria", "valor"}.issubset(df.columns):
        raise HTTPException(status_code=400,
                            detail="O CSV precisa das colunas 'categoria' e 'valor'.")

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    # grava no banco (Mongo ou Postgres) conforme BACKEND
    await persist_dataframe(df, table_name="records")

    # métricas de retorno (pandas)
    totals = {
        "total_geral": float(df["valor"].sum()),
        "media_geral": float(df["valor"].mean()),
        "contagem_geral": int(df["valor"].count())
    }
    agregados = (
        df.groupby("categoria")["valor"]
          .agg(sum="sum", mean="mean", count="count")
          .reset_index()
          .to_dict("records")
    )
    return {**totals, "agregados_por_categoria": agregados}
