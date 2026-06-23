from pathlib import Path
import math

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


MODELO_PATH = Path(__file__).with_name("modelo_cotizacion.pkl")
MODELO_VERSION = 2


def _estimar_area_mueble_m2(largo_mm, ancho_mm, alto_mm, cantidad_piezas):
    area_caja = (
        (2 * alto_mm * ancho_mm)
        + (2 * largo_mm * ancho_mm)
        + (largo_mm * alto_mm)
    ) * 0.000001
    area_piezas = cantidad_piezas * largo_mm * ancho_mm * 0.000001
    return max(float(area_caja), float(area_piezas))


def _crear_features(largo_mm, ancho_mm, alto_mm, cantidad_piezas, precio_material, largo_tablero_mm, ancho_tablero_mm):
    area_mueble_m2 = _estimar_area_mueble_m2(largo_mm, ancho_mm, alto_mm, cantidad_piezas)
    area_tablero_m2 = max(largo_tablero_mm * ancho_tablero_mm * 0.000001, 0.01)
    tableros_estimados = math.ceil((area_mueble_m2 * 1.15) / area_tablero_m2)
    volumen_m3 = largo_mm * ancho_mm * alto_mm * 0.000000001
    return np.array(
        [[area_mueble_m2, area_tablero_m2, tableros_estimados, cantidad_piezas, precio_material, volumen_m3]]
    )


def _precio_base(largo_mm, ancho_mm, alto_mm, cantidad_piezas, precio_material, largo_tablero_mm, ancho_tablero_mm):
    features = _crear_features(
        largo_mm,
        ancho_mm,
        alto_mm,
        cantidad_piezas,
        precio_material,
        largo_tablero_mm,
        ancho_tablero_mm,
    )[0]
    _area_mueble_m2, _area_tablero_m2, tableros_estimados, piezas, precio_unitario, volumen_m3 = features
    costo_material = tableros_estimados * precio_unitario
    mano_obra = 180 + (piezas * 18) + (volumen_m3 * 90)
    return costo_material * 1.55 + mano_obra


def entrenar_modelo_si_no_existe():
    if MODELO_PATH.exists():
        try:
            paquete = joblib.load(MODELO_PATH)
            if paquete.get("version") == MODELO_VERSION:
                return
        except Exception:
            pass

    rng = np.random.default_rng(2024)
    largo = rng.uniform(450, 2600, 450)
    ancho = rng.uniform(300, 900, 450)
    alto = rng.uniform(400, 2400, 450)
    cantidad = rng.integers(2, 31, 450)
    precio_material = rng.uniform(90, 520, 450)
    area_tablero = rng.uniform(2.9, 4.8, 450)

    area_caja = ((2 * alto * ancho) + (2 * largo * ancho) + (largo * alto)) * 0.000001
    area_piezas = cantidad * largo * ancho * 0.000001
    area_mueble = np.maximum(area_caja, area_piezas)
    tableros_estimados = np.ceil((area_mueble * 1.15) / area_tablero)
    volumen = largo * ancho * alto * 0.000000001
    ruido = rng.normal(0, 90, 450)
    precio_total = (tableros_estimados * precio_material * 1.55) + 180 + (cantidad * 18) + (volumen * 90) + ruido
    precio_total = np.maximum(precio_total, 180)

    x = np.column_stack([area_mueble, area_tablero, tableros_estimados, cantidad, precio_material, volumen])
    y = precio_total

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=2024,
    )
    modelo = LinearRegression()
    modelo.fit(x_train, y_train)
    r2 = float(r2_score(y_test, modelo.predict(x_test)))

    joblib.dump({"version": MODELO_VERSION, "modelo": modelo, "r2": max(0.0, min(1.0, r2))}, MODELO_PATH)


def predecir_precio(largo_mm, ancho_mm, alto_mm, cantidad_piezas, precio_material, largo_tablero_mm, ancho_tablero_mm):
    entrenar_modelo_si_no_existe()
    paquete = joblib.load(MODELO_PATH)
    modelo = paquete["modelo"]
    entrada = _crear_features(
        largo_mm,
        ancho_mm,
        alto_mm,
        cantidad_piezas,
        precio_material,
        largo_tablero_mm,
        ancho_tablero_mm,
    )
    precio = float(modelo.predict(entrada)[0])
    precio_minimo = _precio_base(
        largo_mm,
        ancho_mm,
        alto_mm,
        cantidad_piezas,
        precio_material,
        largo_tablero_mm,
        ancho_tablero_mm,
    )
    precio = max(precio, precio_minimo * 0.9, 180.0)
    return round(precio, 2), round(float(paquete["r2"]), 4)
