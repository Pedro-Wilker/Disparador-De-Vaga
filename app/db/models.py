from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nome = Column(String)
    
    senha_hash = Column(String, nullable=True) 
    
    google_id = Column(String, unique=True, nullable=True)
    
    candidaturas = relationship("Candidatura", back_populates="dono")

class Candidatura(Base):
    __tablename__ = "candidaturas"

    id = Column(Integer, primary_key=True, index=True)
    data_envio = Column(DateTime, default=datetime.utcnow)
    destinatario = Column(String, index=True)
    assunto = Column(String)
    status = Column(String, default="Aguardando")
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("Usuario", back_populates="candidaturas")