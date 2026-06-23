from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine
from ml.modelo import entrenar_modelo_si_no_existe
from routers import auth, cortes, cotizaciones, materiales
from routers.auth import crear_password_hash


app = FastAPI(
    title="ALVID API",
    description="API para cotizaciones con Machine Learning y planes de corte FFD.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def crear_datos_iniciales(db: Session):
    if db.query(models.Material).count() == 0:
        db.add_all(
            [
                models.Material(
                    nombre="Melamina blanca 18 mm",
                    tipo="melamina",
                    largo_mm=2440,
                    ancho_mm=1830,
                    espesor_mm=18,
                    precio_unitario_bs=285,
                    stock=18,
                ),
                models.Material(
                    nombre="MDF crudo 15 mm",
                    tipo="MDF",
                    largo_mm=2440,
                    ancho_mm=1220,
                    espesor_mm=15,
                    precio_unitario_bs=210,
                    stock=12,
                ),
                models.Material(
                    nombre="Tablero terciado 18 mm",
                    tipo="tablero",
                    largo_mm=2440,
                    ancho_mm=1220,
                    espesor_mm=18,
                    precio_unitario_bs=245,
                    stock=9,
                ),
            ]
        )

    admin = db.query(models.Usuario).filter(models.Usuario.email == "admin@alvid.com").first()
    if not admin:
        db.add(
            models.Usuario(
                nombre="Administrador ALVID",
                email="admin@alvid.com",
                password_hash=crear_password_hash("alvid2024"),
                rol="admin",
                activo=True,
            )
        )
    db.commit()


@app.on_event("startup")
def iniciar_aplicacion():
    Base.metadata.create_all(bind=engine)
    entrenar_modelo_si_no_existe()
    db = SessionLocal()
    try:
        crear_datos_iniciales(db)
    finally:
        db.close()


@app.get("/")
def healthcheck():
    return {"mensaje": "API ALVID funcionando correctamente"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(materiales.router, prefix="/api/materiales", tags=["materiales"])
app.include_router(cotizaciones.router, prefix="/api/cotizaciones", tags=["cotizaciones"])
app.include_router(cortes.router, prefix="/api/cortes", tags=["cortes"])
