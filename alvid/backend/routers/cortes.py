import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from ml.ffd import ffd
from routers.auth import get_current_user
from schemas import CorteGenerarRequest, PlanCorteOut


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/generar", response_model=PlanCorteOut, status_code=201)
def generar_plan_corte(datos: CorteGenerarRequest, db: Session = Depends(get_db)):
    cotizacion = db.get(models.Cotizacion, datos.cotizacion_id)
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotizacion no encontrada")

    tablero_material = db.get(models.Material, datos.tablero_id)
    if not tablero_material:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")

    tablero = {"largo": tablero_material.largo_mm, "ancho": tablero_material.ancho_mm}
    piezas = [pieza.model_dump() for pieza in datos.piezas]
    try:
        resultado = ffd(piezas, tablero)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    plan = models.PlanCorte(
        cotizacion_id=cotizacion.id,
        tableros_necesarios=resultado["total_tableros"],
        eficiencia_porcentaje=resultado["eficiencia_pct"],
        desperdicio_porcentaje=resultado["desperdicio_pct"],
        detalle_json=json.dumps(resultado),
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    return {
        "id": plan.id,
        "cotizacion_id": plan.cotizacion_id,
        "tableros_necesarios": plan.tableros_necesarios,
        "eficiencia_porcentaje": plan.eficiencia_porcentaje,
        "desperdicio_porcentaje": plan.desperdicio_porcentaje,
        "detalle_json": resultado,
        "created_at": plan.created_at,
    }


@router.get("/cotizacion/{cotizacion_id}", response_model=list[PlanCorteOut])
def listar_planes_por_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    planes = (
        db.query(models.PlanCorte)
        .filter(models.PlanCorte.cotizacion_id == cotizacion_id)
        .order_by(models.PlanCorte.created_at.desc())
        .all()
    )
    return [
        {
            "id": plan.id,
            "cotizacion_id": plan.cotizacion_id,
            "tableros_necesarios": plan.tableros_necesarios,
            "eficiencia_porcentaje": plan.eficiencia_porcentaje,
            "desperdicio_porcentaje": plan.desperdicio_porcentaje,
            "detalle_json": json.loads(plan.detalle_json),
            "created_at": plan.created_at,
        }
        for plan in planes
    ]
