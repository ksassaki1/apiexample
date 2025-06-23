# app/main.py
from fastapi import FastAPI
from app.api.v1.routes_upload import router as upload_router

app = FastAPI()
app.include_router(upload_router, prefix="/v1")
