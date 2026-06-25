from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime
from .database import engine, Base, SessionLocal
from .routers import usuarios, produtos, pedidos, pagamentos, fidelidade, unidades, estoque
from . import models, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API Back-End para o Projeto Multidisciplinar",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Seed automático para facilitar testes e avaliações do tutor
        unidade_exist = db.query(models.Unidade).first()
        if not unidade_exist:
            unidade = models.Unidade(nome="Matriz Recife", endereco="Av. Boa Viagem, 100")
            db.add(unidade)
            db.commit()
            db.refresh(unidade)
            
            produto = models.Produto(nome="Tapioca", descricao="Tapioca de queijo", preco=15.0)
            db.add(produto)
            db.commit()
            db.refresh(produto)
            
            estoque = models.Estoque(produto_id=produto.id, unidade_id=unidade.id, quantidade=100)
            db.add(estoque)
            
            senha_hash = auth.get_password_hash("123456")
            admin = models.Usuario(nome="Admin", email="admin@raizes.com", senha_hash=senha_hash, perfil=models.PerfilEnum.ADMIN)
            db.add(admin)
            
            db.commit()
    finally:
        db.close()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "API_ERROR",
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Erro de validação nos dados enviados.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": request.url.path
        }
    )

app.include_router(usuarios.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(fidelidade.router)
app.include_router(estoque.router)
app.include_router(unidades.router)

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Raízes do Nordeste. Acesse /docs para a documentação."}
