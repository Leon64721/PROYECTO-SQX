#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix #7 (2026-09-11) sobre el proyecto ORB -- ver PropFirm_Management/24_...md.

Cuarta corrida completa consecutiva con 0 sobrevivientes en OOS (1800 -> 0), esta vez con la
ventana ORB ya bien anclada a la apertura NY real (16:30 EET, fix v3) -- descarta definitivamente
la ventana como causa.

Causa raiz (documentada, no supuesta): la condicion de aceptacion de OOS en Retest-Task1.xml exige
`DrawdownPct < 8` sobre la ventana OOS (2023-2026, 3 anios). Verificado contra la Skill 1
(01_SKILL_1_GENERADOR_CFX...md, S40 "Modos de generacion actualizados"):

  DISCOVERY (exploracion inicial de edge desconocido -- exactamente este caso):
    DrawdownPct <= 35 a 45
  BALANCEADO PRODUCTIVO:
    DrawdownPct <= 25 a 32
  ESTRICTO / QUALITY FIRST (para cuando ya se tiene abundancia y se busca menos cantidad,
  mas calidad -- la skill lista textualmente "Cuando OOS = 0" como sintoma de que YA se esta
  en este modo sin haberlo elegido):
    DrawdownPct <= 18 a 28

8% esta MUY por debajo incluso del piso mas estricto documentado (18%) -- viene heredado de la
base MASTER_CLEAN (calibrada para un portafolio ya curado y maduro), no de un analisis para esta
exploracion de un bloque custom recien creado. Es, con alta probabilidad, el principal responsable
del 0/1800 en las 4 corridas reales (la ventana ya se descarto como causa en las corridas v3).

Fix (minimo, una sola variable a la vez -- no tocar NumberOfTrades/AvgTrade/PF/ReturnDDRatio
todavia, para poder aislar el efecto real de este cambio antes de tocar mas cosas):
  DrawdownPct < 8  ->  DrawdownPct < 35   (piso inferior del rango DISCOVERY documentado)

Opera sobre una copia fresca del project.cfx vivo. NO toca el proyecto vivo directamente.
"""
import re
import shutil
import zipfile
import os

LIVE_PROJECT = r"C:\SQX_144_Full\user\projects\BASE_CP_MASTER_CLEAN_V1\project.cfx"
WORK = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\_work_fix_orb_oos_threshold_v4"
OUT = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\BASE_CP_MASTER_CLEAN_V1_ORB_V4_DISCOVERY_DD35.cfx"


def fix_drawdown_condition(txt):
    # Match only the Condition block whose Left-Side is DrawdownPct, then replace ONLY its own
    # Numeric-Value -- avoids touching any other "8" elsewhere in the file.
    pattern = re.compile(
        r'(<Condition use="true">\s*<Left-Side valueType="column">\s*'
        r'<Column-Value column="DrawdownPct"[^/]*/>\s*</Left-Side>\s*'
        r'<Comparator value="&lt;" />\s*<Right-Side valueType="numeric">\s*'
        r'<Numeric-Value value=")8(" />\s*</Right-Side>\s*</Condition>)',
        re.S,
    )
    new_txt, n = pattern.subn(r'\g<1>35\g<2>', txt)
    return new_txt, n


def main():
    if not os.path.exists(LIVE_PROJECT):
        raise SystemExit(f"No se encontro el proyecto vivo en {LIVE_PROJECT} -- ajustar la ruta.")

    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    os.makedirs(WORK)

    with zipfile.ZipFile(LIVE_PROJECT, "r") as zf:
        zf.extractall(WORK)

    path = os.path.join(WORK, "Retest-Task1.xml")
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    new_txt, n = fix_drawdown_condition(txt)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_txt)

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(WORK):
            zf.write(os.path.join(WORK, fname), fname)

    print(f"DrawdownPct OOS: 8 -> 35 (piso DISCOVERY documentado en Skill 1 S40.1): {n} reemplazo (esperado: 1)")
    print(f"Salida: {OUT}")


if __name__ == "__main__":
    main()
