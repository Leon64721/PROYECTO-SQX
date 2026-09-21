#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix #6 (2026-09-09) sobre el proyecto ORB -- ver PropFirm_Management/24_...md, segundo addendum.

Causa raiz: el fix v2 (fix_orb_window_v2.py) angosto la ventana randomizada de #Int1#-#Int4#
(Range Start/End Hour) a bandas "genericas" (Start Hour 6-10, End Hour 10-14) pensadas en terminos
de horas tipo UTC, SIN verificar la zona horaria real del feed. El usuario pregunto por que el
panel "Trading options" no marcaba la sesion NY -- investigando se confirmo que SI esta bien
configurada (MarketOpenSession="No Session" es correcto porque la restriccion real la hace
"Limit Time Range" 16:30-22:30, ya alineado con la apertura NY real en la zona horaria del feed).

Pero esa misma investigacion revelo que la simbologia `NDXm_TICK_UTCPlus02` usa
`timezone="EET"` (Europa del Este) en su definicion de Resources, NO UTC. La apertura del mercado
de NY (9:30 AM hora del Este) cae consistentemente a las 16:30 EET (offset de 7 horas se mantiene
casi todo el ano porque US y UE aplican horario de verano en fechas similares) -- coincide
exactamente con el "Limit Time Range" ya configurado en el proyecto. La ventana v2 (6-10h/10-14h)
NUNCA estuvo cerca de eso -- correspondia a la madrugada/premercado NY, no a la apertura real.

Fix: reanclar #Int1#/#Int3# (Range Start/End Hour) a la apertura real en EET:
  Start Hour: 16 (fijo -- la apertura real es 16:30 EET, no tiene sentido variar la hora)
  Start Minute: sin cambio (0-59) -- deja que el GA explore el minuto exacto alrededor de la apertura
  End Hour: 16-17 (banda que cubre desde el mismo minuto de apertura hasta ~1h45min despues)
  End Minute: sin cambio (0-59)

Esto garantiza End>=Start en todos los casos (Start Hour fijo en 16, End Hour siempre >=16), y
ancla el rango de apertura a la ventana NY real en la zona horaria correcta del feed.

Opera sobre una copia fresca del project.cfx vivo. NO toca el proyecto vivo directamente.
"""
import shutil
import zipfile
import os

LIVE_PROJECT = r"C:\SQX_144_Full\user\projects\BASE_CP_MASTER_CLEAN_V1\project.cfx"
WORK = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\_work_fix_orb_window_v3"
OUT = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\BASE_CP_MASTER_CLEAN_V1_ORBWINDOW_V3.cfx"

OLD_START_HOUR = '<Param key="#Int1#" name="Range Start Hour" type="int" paramType="null" generation="random" minValue="6" maxValue="10" step="1" />'
NEW_START_HOUR = '<Param key="#Int1#" name="Range Start Hour" type="int" paramType="null" generation="random" minValue="16" maxValue="16" step="1" />'

OLD_END_HOUR = '<Param key="#Int3#" name="Range End Hour" type="int" paramType="null" generation="random" minValue="10" maxValue="14" step="1" />'
NEW_END_HOUR = '<Param key="#Int3#" name="Range End Hour" type="int" paramType="null" generation="random" minValue="16" maxValue="17" step="1" />'


def main():
    if not os.path.exists(LIVE_PROJECT):
        raise SystemExit(f"No se encontro el proyecto vivo en {LIVE_PROJECT} -- ajustar la ruta.")

    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    os.makedirs(WORK)

    with zipfile.ZipFile(LIVE_PROJECT, "r") as zf:
        zf.extractall(WORK)

    path = os.path.join(WORK, "Build-Task1.xml")
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    n_start = txt.count(OLD_START_HOUR)
    n_end = txt.count(OLD_END_HOUR)
    txt = txt.replace(OLD_START_HOUR, NEW_START_HOUR)
    txt = txt.replace(OLD_END_HOUR, NEW_END_HOUR)

    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(WORK):
            zf.write(os.path.join(WORK, fname), fname)

    print(f"Start Hour reanclado (6-10 -> 16, apertura NY real en EET): {n_start} reemplazos (esperado: 2)")
    print(f"End Hour reanclado (10-14 -> 16-17): {n_end} reemplazos (esperado: 2)")
    print(f"Salida: {OUT}")


if __name__ == "__main__":
    main()
