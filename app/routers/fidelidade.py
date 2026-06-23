from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from .. import schemas, models, auth, database

logger = logging.getLogger("auditoria")
router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])

@router.get("/saldo")
def obter_saldo(db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    # Mocking saldo
    return {"usuario_id": current_user.id, "saldo_pontos": 150}

@router.post("/resgatar")
def resgatar_pontos(pontos: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    if pontos > 150:
        raise HTTPException(status_code=400, detail="Saldo insuficiente.")
    logger.info(f"Usuário {current_user.id} RESGATOU {pontos} pontos de fidelidade.")
    return {"detail": "Pontos resgatados com sucesso.", "saldo_restante": 150 - pontos}
