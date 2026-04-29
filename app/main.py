from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import init_db
from app.routes import analyze

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup - Executado ao iniciar a aplicação
    print("Inicializando o banco de dados...")
    init_db()
    yield
    # Cleanup - Executado ao encerrar (não necessário aqui)

app = FastAPI(
    title="Log AI Debugger",
    description="Agente de IA que analisa logs de aplicação e diagnostica causas e soluções.",
    version="1.0.0",
    lifespan=lifespan
)

# Registrando as rotas
app.include_router(analyze.router, tags=["Análise de Logs"])

@app.get("/")
def root():
    return {"message": "Bem-vindo ao Log AI Debugger. Acesse /docs para ver a documentação interativa."}
