#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix real, con causa raiz confirmada, de los 3 bugs fatales encontrados el 2026-09-02 en
ORB_MTF_Project.cfx (auditoria /investigate, ver user/PropFirm_Management/24_...md):

1. Build-Task1.xml: los bloques custom CBlock_ORBLongBreakout/CBlock_ORBShortBreakout se
   inyectaron como <Block .../> vacios, sin el hijo <Generated> que SQX exige para cualquier
   bloque custom referenciado en <BuildingBlocks>. Confirmado por el log real:
   "Error: Block 'CBlock_ORBLongBreakout' doesn't contain <Generated> child!, in setting: Blocks"
   y por comparacion byte a byte contra un bloque nativo (EnterAtMarket) que si tiene <Generated>.

2. Build-Task1.xml: <StrategyType additionalCharts="1" .../> declara que las estrategias
   generadas necesitan 1 chart adicional, pero NINGUN bloque activo (todos los signals nativos
   estan use="false", solo los 2 bloques ORB estan activos y ambos usan un unico #Chart1#) usa
   realmente un segundo chart. Esto causaba en OOS: "Not enough additional charts defined."
   Fix: additionalCharts -> 0, alineado con el uso real confirmado.

3. Retest-Task2.xml (MC_TRADES): el Input databank apunta a
   "GESTION MONETARIA - DESACTIVADA" (tarea inactiva, siempre vacia) en vez de "OOS" -- mismo
   patron de bug que el incidente #21 de ayer (STRATEGY QUANT/user/PropFirm_Management). El resto
   de la cadena (MC_SPREAD_SLIPPAGE->TICK->SPP->WFA MATRIX) ya estaba bien encadenada.

4. Retest-Task7.xml: WFA Matrix exigia robMinComb="9" (9 de 9 combinaciones, 100%) -- decision de
   metodologia confirmada como excesivamente estricta con el usuario; se relaja a robMinComb="7"
   (permite 2 fallos de 9), manteniendo robCombRows="3" robCombCols="3" (el tamano de matriz 3x3
   en si no era el problema).

NO toca el proyecto vivo en C:\\SQX_144_Full\\user\\projects\\BASE_CP_MASTER_CLEAN_V1\\ -- escribe
un .cfx nuevo para que el usuario lo importe y confirme antes de reemplazar nada instalado.
"""
import re
import shutil
import zipfile
import os

SRC = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\ORB_MTF_Project.cfx"
WORK = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\_work_fix_orb"
OUT = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\ORB_MTF_Project_FIXED.cfx"

TASK_FILES = ["Build-Task1.xml", "Retest-Task1.xml", "Retest-Task2.xml", "Retest-Task3.xml",
              "Retest-Task4.xml", "Retest-Task5.xml", "Retest-Task6.xml", "Retest-Task7.xml",
              "config.xml"]

# ---- Fix #1: <Generated> para los 2 bloques custom ORB ----
# Parametros tomados literalmente de C:\SQX_144_Full\user\settings\customBlocks.xml
# (misma forma que #Chart1# en cada bloque; Int1-4 = Range Start/End Hour/Minute).
GENERATED_TEMPLATE = (
    '<Generated weight="1">'
    '<Param key="#Chart1#" name="Chart" type="data" paramType="null" generation="random" '
    'minValue="null" maxValue="null" step="null" allCharts="true" />'
    '<Param key="#Int1#" name="Range Start Hour" type="int" paramType="null" generation="random" '
    'minValue="0" maxValue="23" step="1" />'
    '<Param key="#Int2#" name="Range Start Minute" type="int" paramType="null" generation="random" '
    'minValue="0" maxValue="59" step="1" />'
    '<Param key="#Int3#" name="Range End Hour" type="int" paramType="null" generation="random" '
    'minValue="0" maxValue="23" step="1" />'
    '<Param key="#Int4#" name="Range End Minute" type="int" paramType="null" generation="random" '
    'minValue="0" maxValue="59" step="1" />'
    '</Generated>'
)


def fix_generated_blocks(txt):
    before = txt.count('<Block key="CBlock_ORBLongBreakout" weight="1" use="true" category="signals" />')
    before += txt.count('<Block key="CBlock_ORBShortBreakout" weight="1" use="true" category="signals" />')
    txt = txt.replace(
        '<Block key="CBlock_ORBLongBreakout" weight="1" use="true" category="signals" />',
        f'<Block key="CBlock_ORBLongBreakout" weight="1" use="true" category="signals">{GENERATED_TEMPLATE}</Block>'
    )
    txt = txt.replace(
        '<Block key="CBlock_ORBShortBreakout" weight="1" use="true" category="signals" />',
        f'<Block key="CBlock_ORBShortBreakout" weight="1" use="true" category="signals">{GENERATED_TEMPLATE}</Block>'
    )
    return txt, before


def fix_additional_charts(txt):
    n = txt.count('additionalCharts="1"')
    txt = txt.replace(
        '<StrategyType type="simple" additionalCharts="1" templateFile="SQ3StrategyTemplateExample.sq4" improveType="strategy" strategyFile="__STRATEGY_FILE__" architecture="sq4" improveDatabank="Results" />',
        '<StrategyType type="simple" additionalCharts="0" templateFile="SQ3StrategyTemplateExample.sq4" improveType="strategy" strategyFile="__STRATEGY_FILE__" architecture="sq4" improveDatabank="Results" />'
    )
    return txt, n


def fix_databank_chain(txt):
    n = txt.count('value="GESTION MONETARIA - DESACTIVADA"')
    # Solo dentro del bloque real de ruteo (retestSelected="false"); esta cadena no aparece
    # en ningun otro contexto legitimo de Retest-Task2.xml.
    txt = txt.replace(
        '<Databank label="Input databank" name="Input" value="GESTION MONETARIA - DESACTIVADA" />',
        '<Databank label="Input databank" name="Input" value="OOS" />'
    )
    return txt, n


def fix_wfa_strictness(txt):
    n = txt.count('robMinComb="9"')
    txt = txt.replace('robMinComb="9"', 'robMinComb="7"')
    return txt, n


def main():
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    os.makedirs(WORK)

    with zipfile.ZipFile(SRC, "r") as zf:
        zf.extractall(WORK)

    counts = {"generated": 0, "additionalCharts": 0, "databank_chain": 0, "wfa_strictness": 0}

    for fname in TASK_FILES:
        path = os.path.join(WORK, fname)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()

        if fname == "Build-Task1.xml":
            txt, n1 = fix_generated_blocks(txt)
            counts["generated"] += n1
            txt, n2 = fix_additional_charts(txt)
            counts["additionalCharts"] += n2
        elif fname == "Retest-Task2.xml":
            txt, n3 = fix_databank_chain(txt)
            counts["databank_chain"] += n3
        elif fname == "Retest-Task7.xml":
            txt, n4 = fix_wfa_strictness(txt)
            counts["wfa_strictness"] += n4

        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(WORK):
            zf.write(os.path.join(WORK, fname), fname)

    print("Fixes aplicados:")
    print(f"  <Generated> agregado a bloques ORB: {counts['generated']} (esperado: 2)")
    print(f"  additionalCharts 1->0: {counts['additionalCharts']} (esperado: 1)")
    print(f"  Databank chain MC_TRADES Input corregido: {counts['databank_chain']} (esperado: 1)")
    print(f"  WFA robMinComb 9->7: {counts['wfa_strictness']} (esperado: 1)")
    print(f"Salida: {OUT}")


if __name__ == "__main__":
    main()
