from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from routers.auth import get_current_user
from schemas import MaterialCreate, MaterialOut, MaterialUpdate


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[MaterialOut])
def listar_materiales(db: Session = Depends(get_db)):
    return db.query(models.Material).order_by(models.Material.nombre.asc()).all()


@router.post("/", response_model=MaterialOut, status_code=201)
def crear_material(datos: MaterialCreate, db: Session = Depends(get_db)):
    material = models.Material(**datos.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@router.get("/{material_id}", response_model=MaterialOut)
def obtener_material(material_id: int, db: Session = Depends(get_db)):
    material = db.get(models.Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return material


@router.put("/{material_id}", response_model=MaterialOut)
def actualizar_material(material_id: int, datos: MaterialUpdate, db: Session = Depends(get_db)):
    material = db.get(models.Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(material, campo, valor)
    db.commit()
    db.refresh(material)
    return material


@router.delete("/{material_id}")
def eliminar_material(material_id: int, db: Session = Depends(get_db)):
    material = db.get(models.Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    db.delete(material)
    db.commit()
    return {"mensaje": "Material eliminado correctamente"}
