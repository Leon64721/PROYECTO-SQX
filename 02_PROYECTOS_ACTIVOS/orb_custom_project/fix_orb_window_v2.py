#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix #5 (2026-09-09) sobre el proyecto ORB -- ver PropFirm_Management/24_...md, addendum.

Causa raiz confirmada DOS VECES con evidencia real (09-02 y 09-06, ambas corridas reales de
OOS sobre las 1800 estrategias de Results, sin errores, 0 sobrevivientes ambas veces): el fix
del 2026-09-02 dejo que el Builder randomizara la ventana de "opening range" de
CBlock_ORBLongBreakout/CBlock_ORBShortBreakout en TODO el espacio de 24 horas / 60 minutos
(#Int1#-#Int4# = Range Start/End Hour/Minute), produciendo mayormente rangos sin sentido
economico (ej. de 22:47 a 3:12) en vez de una apertura de sesion real. El default original del
propio bloque en customBlocks.xml (9:30-10:00, apertura NY) era correcto; el <Generated> nunca
lo aprovecho.

Fix: angostar el rango aleatorio a bandas que garantizan End Hour >= Start Hour en la enorme
mayoria de combinaciones, cubriendo aperturas de sesion reales (pre-Londres a mediodia NY):
  Start Hour: 6-10 (antes 0-23)
  Start Minute: sin cambio (0-59)
  End Hour: 10-14 (antes 0-23) -- banda que nunca baja del techo de Start Hour
  End Minute: sin cambio (0-59)

Opera sobre una copia FRESCA del project.cfx que este corriendo en SQX en el momento de ejecutar
este script (para no perder ajustes hechos a mano en la UI desde el 09-02, ej. cambio de simbolo
a NDXm_TICK_UTCPlus02/M30). NO toca el proyecto vivo directamente -- escribe un .cfx nuevo.
"""
import shutil
import zipfile
import os

LIVE_PROJECT = r"C:\SQX_144_Full\user\projects\BASE_CP_MASTER_CLEAN_V1\project.cfx"
WORK = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\_work_fix_orb_window_v2"
OUT = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\BASE_CP_MASTER_CLEAN_V1_ORBWINDOW_V2.cfx"

OLD_START_HOUR = '<Param key="#Int1#" name="Range Start Hour" type="int" paramType="null" generation="random" minValue="0" maxValue="23" step="1" />'
NEW_START_HOUR = '<Param key="#Int1#" name="Range Start Hour" type="int" paramType="null" generation="random" minValue="6" maxValue="10" step="1" />'

OLD_END_HOUR = '<Param key="#Int3#" name="Range End Hour" type="int" paramType="null" generation="random" minValue="0" maxValue="23" step="1" />'
NEW_END_HOUR = '<Param key="#Int3#" name="Range End Hour" type="int" paramType="null" generation="random" minValue="10" maxValue="14" step="1" />'


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

    print(f"Start Hour angostado (0-23 -> 6-10): {n_start} reemplazos (esperado: 2, uno por bloque ORB)")
    print(f"End Hour angostado (0-23 -> 10-14): {n_end} reemplazos (esperado: 2)")
    print(f"Salida: {OUT}")


if __name__ == "__main__":
    main()
