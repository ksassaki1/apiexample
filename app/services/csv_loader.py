import io
import pandas as pd
from fastapi import UploadFile

CHUNK_SIZE = 50_000  # ajustável

async def csv_to_dataframe(file: UploadFile) -> pd.DataFrame:
    # lê em memória se for pequeno; caso contrário, em chunks
    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except pd.errors.EmptyDataError:
        raise ValueError("CSV vazio")
    return df
