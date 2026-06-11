from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
import app.db.models as models

from app.api.routes import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobPilot API",
    description="API robusta para gestão de candidaturas e disparos de e-mail.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"status": "online", "mensagem": "JobPilot API rodando com sucesso! 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)