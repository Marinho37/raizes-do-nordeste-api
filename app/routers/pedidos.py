from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from .. import schemas, models, auth, database

logger = logging.getLogger("auditoria")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - AUDITORIA - %(message)s")

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=schemas.PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    pedido_in: schemas.PedidoCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Validar canal de pedido
    if not pedido_in.canalPedido:
        raise HTTPException(status_code=422, detail="canalPedido é obrigatório.")
        
    total_pedido = 0.0
    itens_obj = []
    
    for item in pedido_in.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id, models.Produto.ativo == 1).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto com ID {item.produto_id} não encontrado ou inativo.")
        
        # Simulação simples de estoque (na prática, abateria aqui)
        
        preco_item = produto.preco
        total_pedido += preco_item * item.quantidade
        
        itens_obj.append(models.ItemPedido(
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=preco_item
        ))

    novo_pedido = models.Pedido(
        usuario_id=current_user.id,
        canal_pedido=pedido_in.canalPedido,
        total=total_pedido,
        status=models.StatusPedidoEnum.CRIADO
    )
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    
    for item_obj in itens_obj:
        item_obj.pedido_id = novo_pedido.id
        db.add(item_obj)
        
    db.commit()
    db.refresh(novo_pedido)
    
    logger.info(f"Usuário {current_user.id} CRIOU o pedido {novo_pedido.id} no canal {novo_pedido.canal_pedido}.")
    
    return novo_pedido

@router.get("/", response_model=List[schemas.PedidoResponse])
def listar_pedidos(
    canalPedido: Optional[models.CanalPedidoEnum] = None,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    query = db.query(models.Pedido)
    
    # Se cliente, vê apenas os próprios
    if current_user.perfil == models.PerfilEnum.CLIENTE:
        query = query.filter(models.Pedido.usuario_id == current_user.id)
        
    if canalPedido:
        query = query.filter(models.Pedido.canal_pedido == canalPedido)
        
    return query.all()

@router.patch("/{pedido_id}/status")
def atualizar_status(
    pedido_id: int,
    status_data: schemas.AtualizaStatusPedido,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    # Atualiza status livremente para simplificação do MVP
    novo_status = status_data.forma_pagamento.upper()
    try:
        pedido.status = models.StatusPedidoEnum(novo_status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Status inválido.")
        
    db.commit()
    logger.info(f"Usuário {current_user.id} ALTEROU o status do pedido {pedido.id} para {pedido.status}.")
    return {"detail": "Status atualizado.", "novo_status": pedido.status}
