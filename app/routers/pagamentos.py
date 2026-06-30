from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
from .. import schemas, models, auth, database

logger = logging.getLogger("auditoria")
router = APIRouter(prefix="/pagamentos", tags=["Pagamento"])

class PagamentoMock(BaseModel):
    pedido_id: int
    forma_pagamento: str

@router.post("/")
def processar_pagamento(
    pagamento: PagamentoMock,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pagamento.pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
    if pedido.status != models.StatusPedidoEnum.CRIADO:
        raise HTTPException(status_code=400, detail="Pedido não está aguardando pagamento.")
        
    if pagamento.forma_pagamento.upper() == "MOCK":
        pedido.status = models.StatusPedidoEnum.PAGO
        
        # Registra o pagamento no banco
        novo_pag = models.Pagamento(pedido_id=pedido.id, status="APROVADO", forma_pagamento="MOCK", txid="mock-1234")
        db.add(novo_pag)
        
        # Acumula pontos de fidelidade (1 ponto por real gasto)
        fidelidade = db.query(models.Fidelidade).filter(models.Fidelidade.usuario_id == pedido.usuario_id).first()
        if not fidelidade:
            fidelidade = models.Fidelidade(usuario_id=pedido.usuario_id, pontos=0)
            db.add(fidelidade)
        fidelidade.pontos += int(pedido.total)
        
        db.commit()
        logger.info(f"Usuário {current_user.id} REALIZOU PAGAMENTO do pedido {pedido.id} (Mock Gateway).")
        return {"detail": "Pagamento simulado com sucesso via Gateway MOCK.", "novo_status": pedido.status}
    else:
        # Registra tentativa falha se desejar, mas não altera status
        logger.info(f"Usuário {current_user.id} TENTOU pagar pedido {pedido.id} com forma inválida.")
        raise HTTPException(status_code=400, detail="Forma de pagamento inválida. Pagamento recusado.")
