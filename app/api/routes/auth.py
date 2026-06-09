from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.db.models as models
import app.schemas.schemas as schemas
from app.core.security import gerar_hash_senha

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

@router.post("/registrar", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioRegistro, db: Session = Depends(get_db)):
    
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este e-mail já está em uso."
        )

    senha_criptografada = gerar_hash_senha(usuario.senha)

    novo_usuario = models.Usuario(
        email=usuario.email,
        nome=usuario.nome,
        senha_hash=senha_criptografada
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario