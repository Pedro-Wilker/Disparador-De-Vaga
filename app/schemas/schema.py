from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CandidaturaBase(BaseModel):
    destinatario: str
    assunto: str
    status: str = "Aguardando"

class CandidaturaCreate(CandidaturaBase):
    pass

class Candidatura(CandidaturaBase):
    id: int
    data_envio: datetime
    usuario_id: int

    class Config:
        from_attributes = True 
        
class UsuarioBase(BaseModel):
    email: str
    nome: str

class UsuarioCreate(UsuarioBase):
    google_id: Optional[str] = None

class Usuario(UsuarioBase):
    id: int
    candidaturas: List[Candidatura] = [] 

    class Config:
        from_attributes = True
    
class UsuarioRegistro(UsuarioBase):
    senha: str