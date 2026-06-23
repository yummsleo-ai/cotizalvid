from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MaterialBase(BaseModel):
    nombre: str
    tipo: str
    largo_mm: float = Field(gt=0)
    ancho_mm: float = Field(gt=0)
    espesor_mm: float = Field(gt=0)
    precio_unitario_bs: float = Field(gt=0)
    stock: int = Field(ge=0)


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    largo_mm: float | None = Field(default=None, gt=0)
    ancho_mm: float | None = Field(default=None, gt=0)
    espesor_mm: float | None = Field(default=None, gt=0)
    precio_unitario_bs: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class MaterialOut(MaterialBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PrediccionRequest(BaseModel):
    largo_mm: float = Field(gt=0)
    ancho_mm: float = Field(gt=0)
    alto_mm: float = Field(gt=0)
    cantidad_piezas: int = Field(gt=0)
    material_id: int


class PrediccionResponse(BaseModel):
    precio_estimado_bs: float
    confianza: float


class CotizacionBase(BaseModel):
    nombre_cliente: str
    descripcion: str
    tipo_mueble: str
    cantidad_piezas: int = Field(gt=0)
    material_id: int
    largo_mm: float = Field(gt=0)
    ancho_mm: float = Field(gt=0)
    alto_mm: float = Field(gt=0)
    precio_final_bs: float | None = Field(default=None, gt=0)
    estado: str = "pendiente"


class CotizacionCreate(CotizacionBase):
    pass


class CotizacionUpdate(BaseModel):
    nombre_cliente: str | None = None
    descripcion: str | None = None
    tipo_mueble: str | None = None
    cantidad_piezas: int | None = Field(default=None, gt=0)
    material_id: int | None = None
    largo_mm: float | None = Field(default=None, gt=0)
    ancho_mm: float | None = Field(default=None, gt=0)
    alto_mm: float | None = Field(default=None, gt=0)
    precio_final_bs: float | None = Field(default=None, gt=0)
    estado: str | None = None


class CotizacionOut(BaseModel):
    id: int
    nombre_cliente: str
    descripcion: str
    tipo_mueble: str
    cantidad_piezas: int
    material_id: int
    largo_mm: float
    ancho_mm: float
    alto_mm: float
    precio_estimado_ml: float
    precio_final_bs: float
    estado: str
    created_at: datetime
    material: MaterialOut | None = None

    model_config = ConfigDict(from_attributes=True)


class PiezaCorte(BaseModel):
    largo: float = Field(gt=0)
    ancho: float = Field(gt=0)
    cantidad: int = Field(default=1, gt=0)
    etiqueta: str


class CorteGenerarRequest(BaseModel):
    cotizacion_id: int
    piezas: list[PiezaCorte]
    tablero_id: int


class PlanCorteOut(BaseModel):
    id: int
    cotizacion_id: int
    tableros_necesarios: int
    eficiencia_porcentaje: float
    desperdicio_porcentaje: float
    detalle_json: dict[str, Any]
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: dict[str, Any]
