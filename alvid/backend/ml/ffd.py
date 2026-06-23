def _area(pieza):
    return pieza["largo"] * pieza["ancho"]


def _expandir_piezas(piezas):
    expandidas = []
    for pieza in piezas:
        for indice in range(1, int(pieza.get("cantidad", 1)) + 1):
            expandidas.append(
                {
                    "largo": float(pieza["largo"]),
                    "ancho": float(pieza["ancho"]),
                    "etiqueta": f"{pieza['etiqueta']} #{indice}",
                }
            )
    return expandidas


def _limpiar_espacios(espacios):
    validos = [e for e in espacios if e["largo"] > 0 and e["ancho"] > 0]
    resultado = []
    for espacio in validos:
        contenido = False
        for otro in validos:
            if espacio is otro:
                continue
            dentro_x = espacio["x"] >= otro["x"] and espacio["x"] + espacio["largo"] <= otro["x"] + otro["largo"]
            dentro_y = espacio["y"] >= otro["y"] and espacio["y"] + espacio["ancho"] <= otro["y"] + otro["ancho"]
            if dentro_x and dentro_y:
                contenido = True
                break
        if not contenido:
            resultado.append(espacio)
    return sorted(resultado, key=lambda e: (e["y"], e["x"], e["ancho"], e["largo"]))


def _intentar_colocar(tablero, pieza):
    tablero["espacios"].sort(key=lambda e: (e["y"], e["x"]))
    for indice, espacio in enumerate(tablero["espacios"]):
        orientaciones = [
            (pieza["largo"], pieza["ancho"], False),
            (pieza["ancho"], pieza["largo"], True),
        ]
        for largo, ancho, rotada in orientaciones:
            if largo <= espacio["largo"] and ancho <= espacio["ancho"]:
                colocada = {
                    "x": espacio["x"],
                    "y": espacio["y"],
                    "largo": largo,
                    "ancho": ancho,
                    "etiqueta": pieza["etiqueta"],
                    "rotada": rotada,
                }
                tablero["piezas"].append(colocada)
                usados = tablero["espacios"].pop(indice)
                tablero["espacios"].extend(
                    [
                        {
                            "x": usados["x"] + largo,
                            "y": usados["y"],
                            "largo": usados["largo"] - largo,
                            "ancho": ancho,
                        },
                        {
                            "x": usados["x"],
                            "y": usados["y"] + ancho,
                            "largo": usados["largo"],
                            "ancho": usados["ancho"] - ancho,
                        },
                    ]
                )
                tablero["espacios"] = _limpiar_espacios(tablero["espacios"])
                return True
    return False


def _nuevo_tablero(tablero, tablero_id):
    return {
        "id": tablero_id,
        "piezas": [],
        "espacios": [
            {
                "x": 0.0,
                "y": 0.0,
                "largo": float(tablero["largo"]),
                "ancho": float(tablero["ancho"]),
            }
        ],
    }


def ffd(piezas, tablero):
    piezas_ordenadas = sorted(_expandir_piezas(piezas), key=_area, reverse=True)
    tableros = []
    area_tablero = float(tablero["largo"]) * float(tablero["ancho"])

    for pieza in piezas_ordenadas:
        cabe_normal = pieza["largo"] <= tablero["largo"] and pieza["ancho"] <= tablero["ancho"]
        cabe_rotada = pieza["ancho"] <= tablero["largo"] and pieza["largo"] <= tablero["ancho"]
        if not cabe_normal and not cabe_rotada:
            raise ValueError(f"La pieza {pieza['etiqueta']} no cabe en el tablero")
        colocada = False
        for tablero_actual in tableros:
            if _intentar_colocar(tablero_actual, pieza):
                colocada = True
                break
        if not colocada:
            nuevo = _nuevo_tablero(tablero, len(tableros) + 1)
            if not _intentar_colocar(nuevo, pieza):
                raise ValueError(f"La pieza {pieza['etiqueta']} no cabe en el tablero")
            tableros.append(nuevo)

    total_usado = 0.0
    respuesta_tableros = []
    for tablero_actual in tableros:
        usado = sum(_area(pieza) for pieza in tablero_actual["piezas"])
        total_usado += usado
        espacio_usado_pct = round((usado / area_tablero) * 100, 2) if area_tablero else 0
        respuesta_tableros.append(
            {
                "id": tablero_actual["id"],
                "largo": float(tablero["largo"]),
                "ancho": float(tablero["ancho"]),
                "piezas": tablero_actual["piezas"],
                "espacio_usado_pct": espacio_usado_pct,
            }
        )

    capacidad_total = area_tablero * len(tableros)
    eficiencia = round((total_usado / capacidad_total) * 100, 2) if capacidad_total else 0
    desperdicio = round(100 - eficiencia, 2)

    return {
        "tableros": respuesta_tableros,
        "total_tableros": len(tableros),
        "eficiencia_pct": eficiencia,
        "desperdicio_pct": desperdicio,
    }
