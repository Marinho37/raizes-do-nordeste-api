from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registrar", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(user: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")
    
    hashed_password = auth.get_password_hash(user.senha)
    novo_usuario = models.Usuario(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password,
        perfil=user.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginData, db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == login_data.email).first()
    if not user or not auth.verify_password(login_data.senha, user.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.perfil.value})
    return {"access_token": access_token, "token_type": "bearer"}
