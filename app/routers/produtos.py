from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, auth, database

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(database.get_db)):
    return db.query(models.Produto).filter(models.Produto.ativo == 1).all()

@router.post("/", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: schemas.ProdutoCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.require_role(["ADMIN", "GERENTE"]))
):
    novo_produto = models.Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto
