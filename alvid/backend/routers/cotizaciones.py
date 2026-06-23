from collections import Counter, defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

import models
from database import get_db
from ml.modelo import predecir_precio
from routers.auth import get_current_user
from schemas import (
    CotizacionCreate,
    CotizacionOut,
    CotizacionUpdate,
    PrediccionRequest,
    PrediccionResponse,
)


router = APIRouter(dependencies=[Depends(get_current_user)])
ESTADOS_VALIDOS = {"pendiente", "aprobada", "rechazada"}


def _obtener_material(db: Session, material_id: int) -> models.Material:
    material = db.get(models.Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return material


def _calcular_prediccion(db: Session, datos: PrediccionRequest):
    material = _obtener_material(db, datos.material_id)
    precio, confianza = predecir_precio(
        datos.largo_mm,
        datos.ancho_mm,
        datos.alto_mm,
        datos.cantidad_piezas,
        material.precio_unitario_bs,
        material.largo_mm,
        material.ancho_mm,
    )
    return precio, confianza


@router.post("/predecir", response_model=PrediccionResponse)
def predecir_cotizacion(datos: PrediccionRequest, db: Session = Depends(get_db)):
    precio, confianza = _calcular_prediccion(db, datos)
    return {"precio_estimado_bs": precio, "confianza": confianza}


@router.get("/resumen")
def resumen_dashboard(db: Session = Depends(get_db)):
    cotizaciones = (
        db.query(models.Cotizacion)
        .options(joinedload(models.Cotizacion.material))
        .order_by(models.Cotizacion.created_at.desc())
        .all()
    )
    por_estado = Counter(c.estado for c in cotizaciones)
    promedio = (
        round(sum(c.precio_final_bs for c in cotizaciones) / len(cotizaciones), 2)
        if cotizaciones
        else 0
    )
    uso_materiales = Counter(c.material.nombre if c.material else "Sin material" for c in cotizaciones)
    por_mes = defaultdict(int)
    for cotizacion in cotizaciones:
        por_mes[cotizacion.created_at.strftime("%Y-%m")] += 1

    ultimas = [
        {
            "id": cotizacion.id,
            "nombre_cliente": cotizacion.nombre_cliente,
            "tipo_mueble": cotizacion.tipo_mueble,
            "estado": cotizacion.estado,
            "precio_final_bs": cotizacion.precio_final_bs,
            "created_at": cotizacion.created_at,
            "material": cotizacion.material.nombre if cotizacion.material else None,
        }
        for cotizacion in cotizaciones[:5]
    ]

    return {
        "totales_estado": {
            "pendiente": por_estado.get("pendiente", 0),
            "aprobada": por_estado.get("aprobada", 0),
            "rechazada": por_estado.get("rechazada", 0),
        },
        "precio_promedio": promedio,
        "top_materiales": [
            {"nombre": nombre, "total": total}
            for nombre, total in uso_materiales.most_common(3)
        ],
        "ultimas_cotizaciones": ultimas,
        "cotizaciones_por_mes": [
            {"mes": mes, "total": total}
            for mes, total in sorted(por_mes.items())
        ],
    }


@router.get("/", response_model=list[CotizacionOut])
def listar_cotizaciones(db: Session = Depends(get_db)):
    return (
        db.query(models.Cotizacion)
        .options(joinedload(models.Cotizacion.material))
        .order_by(models.Cotizacion.created_at.desc())
        .all()
    )


@router.post("/", response_model=CotizacionOut, status_code=201)
def crear_cotizacion(datos: CotizacionCreate, db: Session = Depends(get_db)):
    if datos.estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado de cotizacion invalido")

    precio_estimado, _confianza = _calcular_prediccion(
        db,
        PrediccionRequest(
            largo_mm=datos.largo_mm,
            ancho_mm=datos.ancho_mm,
            alto_mm=datos.alto_mm,
            cantidad_piezas=datos.cantidad_piezas,
            material_id=datos.material_id,
        ),
    )
    payload = datos.model_dump()
    precio_final = payload.pop("precio_final_bs") or precio_estimado
    cotizacion = models.Cotizacion(
        **payload,
        precio_estimado_ml=precio_estimado,
        precio_final_bs=precio_final,
    )
    db.add(cotizacion)
    db.commit()
    db.refresh(cotizacion)
    return cotizacion


@router.get("/{cotizacion_id}", response_model=CotizacionOut)
def obtener_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = (
        db.query(models.Cotizacion)
        .options(joinedload(models.Cotizacion.material))
        .filter(models.Cotizacion.id == cotizacion_id)
        .first()
    )
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotizacion no encontrada")
    return cotizacion


@router.put("/{cotizacion_id}", response_model=CotizacionOut)
def actualizar_cotizacion(cotizacion_id: int, datos: CotizacionUpdate, db: Session = Depends(get_db)):
    cotizacion = db.get(models.Cotizacion, cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotizacion no encontrada")

    cambios = datos.model_dump(exclude_unset=True)
    if "estado" in cambios and cambios["estado"] not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado de cotizacion invalido")
    if "material_id" in cambios:
        _obtener_material(db, cambios["material_id"])

    for campo, valor in cambios.items():
        setattr(cotizacion, campo, valor)
    db.commit()
    db.refresh(cotizacion)
    return cotizacion


@router.delete("/{cotizacion_id}")
def eliminar_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.get(models.Cotizacion, cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotizacion no encontrada")
    db.delete(cotizacion)
    db.commit()
    return {"mensaje": "Cotizacion eliminada correctamente"}
