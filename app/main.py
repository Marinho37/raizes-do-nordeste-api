from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime
from .database import engine, Base
from .routers import usuarios, produtos, pedidos, fidelidade, unidades, estoque

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API Back-End para o Projeto Multidisciplinar",
    version="1.0.0"
)

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
app.include_router(fidelidade.router)
app.include_router(estoque.router)
app.include_router(unidades.router)

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Raízes do Nordeste. Acesse /docs para a documentação."}
