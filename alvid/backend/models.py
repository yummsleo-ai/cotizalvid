from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Material(Base):
    __tablename__ = "materiales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False)
    largo_mm: Mapped[float] = mapped_column(Float, nullable=False)
    ancho_mm: Mapped[float] = mapped_column(Float, nullable=False)
    espesor_mm: Mapped[float] = mapped_column(Float, nullable=False)
    precio_unitario_bs: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cotizaciones: Mapped[list["Cotizacion"]] = relationship(back_populates="material")


class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_cliente: Mapped[str] = mapped_column(String(160), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    tipo_mueble: Mapped[str] = mapped_column(String(80), nullable=False)
    cantidad_piezas: Mapped[int] = mapped_column(Integer, nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiales.id"), nullable=False)
    largo_mm: Mapped[float] = mapped_column(Float, nullable=False)
    ancho_mm: Mapped[float] = mapped_column(Float, nullable=False)
    alto_mm: Mapped[float] = mapped_column(Float, nullable=False)
    precio_estimado_ml: Mapped[float] = mapped_column(Float, nullable=False)
    precio_final_bs: Mapped[float] = mapped_column(Float, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="pendiente")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    material: Mapped[Material] = relationship(back_populates="cotizaciones")
    planes_corte: Mapped[list["PlanCorte"]] = relationship(back_populates="cotizacion")


class PlanCorte(Base):
    __tablename__ = "plan_cortes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cotizacion_id: Mapped[int] = mapped_column(ForeignKey("cotizaciones.id"), nullable=False)
    tableros_necesarios: Mapped[int] = mapped_column(Integer, nullable=False)
    eficiencia_porcentaje: Mapped[float] = mapped_column(Float, nullable=False)
    desperdicio_porcentaje: Mapped[float] = mapped_column(Float, nullable=False)
    detalle_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cotizacion: Mapped[Cotizacion] = relationship(back_populates="planes_corte")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(30), nullable=False, default="empleado")
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
