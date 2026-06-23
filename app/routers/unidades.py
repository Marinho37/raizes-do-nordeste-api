from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter(prefix="/unidades", tags=["Unidades"])

@router.get("/")
def listar_unidades(db: Session = Depends(database.get_db)):
    unidades = db.query(models.Unidade).all()
    return [{"id": u.id, "nome": u.nome, "endereco": u.endereco} for u in unidades]

@router.get("/{id}/cardapio")
def listar_cardapio_unidade(id: int, db: Session = Depends(database.get_db)):
    unidade = db.query(models.Unidade).filter(models.Unidade.id == id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada.")
    # In a real app this would filter by product available in this unit. For mock we return all active products.
    produtos = db.query(models.Produto).filter(models.Produto.ativo == 1).all()
    return [{"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos]
