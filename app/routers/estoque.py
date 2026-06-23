from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
from .. import schemas, models, auth, database

logger = logging.getLogger("auditoria")
router = APIRouter(prefix="/estoque", tags=["Estoque"])

class Movimentacao(BaseModel):
    produto_id: int
    unidade_id: int
    quantidade: int

@router.get("/{unidadeId}")
def consultar_saldo(unidadeId: int, db: Session = Depends(database.get_db)):
    estoque = db.query(models.Estoque).filter(models.Estoque.unidade_id == unidadeId).all()
    return [{"produto_id": e.produto_id, "quantidade": e.quantidade} for e in estoque]

@router.patch("/movimentar")
def movimentar_estoque(mov: Movimentacao, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(auth.require_role(["ADMIN", "GERENTE"]))):
    estoque = db.query(models.Estoque).filter(
        models.Estoque.unidade_id == mov.unidade_id,
        models.Estoque.produto_id == mov.produto_id
    ).first()
    
    if not estoque:
        estoque = models.Estoque(produto_id=mov.produto_id, unidade_id=mov.unidade_id, quantidade=0)
        db.add(estoque)
        
    estoque.quantidade += mov.quantidade
    if estoque.quantidade < 0:
        raise HTTPException(status_code=400, detail="Estoque não pode ser negativo.")
        
    db.commit()
    logger.info(f"Usuário {current_user.id} MOVIMENTOU estoque do produto {mov.produto_id} na unidade {mov.unidade_id} em {mov.quantidade}.")
    return {"detail": "Movimentação registrada com sucesso.", "novo_saldo": estoque.quantidade}
