from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .models import PerfilEnum, CanalPedidoEnum, StatusPedidoEnum

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str
    perfil: Optional[PerfilEnum] = PerfilEnum.CLIENTE

class UsuarioResponse(UsuarioBase):
    id: int
    perfil: PerfilEnum
    class Config:
        from_attributes = True

class LoginData(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    ativo: int
    class Config:
        from_attributes = True

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    unidade_id: int
    canalPedido: CanalPedidoEnum
    itens: List[ItemPedidoCreate]

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    canal_pedido: CanalPedidoEnum
    status: StatusPedidoEnum
    total: float
    itens: List[ItemPedidoResponse]
    class Config:
        from_attributes = True

class AtualizaStatusPedido(BaseModel):
    forma_pagamento: str
