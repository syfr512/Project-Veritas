import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.endpoints import router as api_router
from app.api.auth import router as auth_router
from app.api.webhooks import router as webhook_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Veritas API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(webhook_router, prefix="/api/webhooks", tags=["enterprise-integration"])

@app.get("/")
def root():
    return {"message": "Project Veritas API is running"}
