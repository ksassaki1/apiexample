# app/services/persistence.py
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import MetaData, Table, Column, Float, String, Integer
from ..core.db import sql_engine, get_settings


async def persist_dataframe(df: pd.DataFrame, table_name: str = "records"):
    settings = get_settings()

    if settings.backend == "mongo":
        from ..core.db import get_mongo_db
        await get_mongo_db()[table_name].insert_many(
            df.where(df.notnull(), None).to_dict("records")
        )
        return

    await dataframe_to_postgres(df, table_name)


async def dataframe_to_postgres(df: pd.DataFrame, table_name: str):
    meta = MetaData()

    # 1) abre transação assíncrona
    async with sql_engine.begin() as conn:

        # ---- reflexão *síncrona* protegida ----
        exists = await conn.run_sync(
            lambda sync_conn: sa.inspect(sync_conn).has_table(table_name)
        )

        if not exists:
            cols=[]
            if "id" not in df.columns:
                cols.append(Column("id", Integer, primary_key=True, autoincrement=True))
            for c, dtype in df.dtypes.items():
                cols.append(Column(c, Float if dtype.kind in "if" else String))
            Table(table_name, meta, *cols)

            # cria somente na primeira vez
            await conn.run_sync(meta.create_all)
        else:
            # reflete esquema existente
            await conn.run_sync(
                lambda sync_conn: meta.reflect(bind=sync_conn, only=[table_name])
            )

    # 2) obtém a tabela refletida
    t = meta.tables[table_name]

    # 3) converte NaN → None e insere linhas
    records = df.where(df.notnull(), None).to_dict("records")
    async with sql_engine.begin() as conn:
        await conn.execute(t.insert(), records)


__all__ = ["persist_dataframe"]
