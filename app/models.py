from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from .database import Base

class PerfilEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    CLIENTE = "CLIENTE"

class CanalPedidoEnum(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    WEB = "WEB"
    PICKUP = "PICKUP"

class StatusPedidoEnum(str, enum.Enum):
    CRIADO = "CRIADO"
    PAGO = "PAGO"
    COZINHA = "COZINHA"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    perfil = Column(SQLEnum(PerfilEnum), default=PerfilEnum.CLIENTE)

class Unidade(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    endereco = Column(String)

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    preco = Column(Float)
    ativo = Column(Integer, default=1)

class Estoque(Base):
    __tablename__ = "estoque"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    quantidade = Column(Integer)
    produto = relationship("Produto")
    unidade = relationship("Unidade")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    canal_pedido = Column(SQLEnum(CanalPedidoEnum))
    status = Column(SQLEnum(StatusPedidoEnum), default=StatusPedidoEnum.CRIADO)
    total = Column(Float, default=0.0)
    itens = relationship("ItemPedido", back_populates="pedido")
    unidade = relationship("Unidade")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    pedido = relationship("Pedido", back_populates="itens")
