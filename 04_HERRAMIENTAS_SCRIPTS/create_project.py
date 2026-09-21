import zipfile
import xml.etree.ElementTree as ET
import os
import shutil
import glob
import copy
import argparse
import sys

base_cfx = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517\07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY_FIXED.cfx'
out_cfx = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\ORB_MTF_Project.cfx'

def configure_money_management(root, mm_type, mm_value):
    for rmm in root.findall('.//RiskMoneyManagement/MoneyManagement'):
        for method in rmm.findall('Method'):
            method.set('use', 'false')
            
        if mm_type == '1':
            fixed_method = rmm.find('Method[@type="FixedSize"]')
            if fixed_method is None:
                fixed_method = ET.SubElement(rmm, 'Method', {'type': 'FixedSize', 'use': 'true'})
                params = ET.SubElement(fixed_method, 'Params')
                param = ET.SubElement(params, 'Param', {'key': 'Size', 'className': 'FixedSize'})
                param.text = str(mm_value)
            else:
                fixed_method.set('use', 'true')
                param = fixed_method.find('.//Param[@key="Size"]')
                if param is not None:
                    param.text = str(mm_value)
                    
        elif mm_type == '2':
            risk_method = rmm.find('Method[@type="RiskFixedBalancePct"]')
            if risk_method is None:
                risk_method = ET.SubElement(rmm, 'Method', {'type': 'RiskFixedBalancePct', 'use': 'true'})
                params = ET.SubElement(risk_method, 'Params')
                param = ET.SubElement(params, 'Param', {'key': 'Risk', 'className': 'RiskFixedBalancePct'})
                param.text = str(mm_value)
            else:
                risk_method.set('use', 'true')
                param = risk_method.find('.//Param[@key="Risk"]')
                if param is not None:
                    param.text = str(mm_value)

def configure_time_filters(root, limit_time='false', time_from='0', time_to='0', exit_eor='false', eod_time='86100'):
    """
    Configura de forma dinámica los filtros de tiempo en TradingOptions.
    Estos valores deben ser inyectados dinámicamente tras calcular la conversión a UTC+2.
    """
    for param in root.findall('.//Param[@key="LimitTimeRange"]'):
        param.text = limit_time
    for param in root.findall('.//Param[@key="SignalTimeRangeFrom"]'):
        param.text = time_from
    for param in root.findall('.//Param[@key="SignalTimeRangeTo"]'):
        param.text = time_to
    for param in root.findall('.//Param[@key="ExitAtEndOfRange"]'):
        param.text = exit_eor
    for param in root.findall('.//Param[@key="ExitAtEndOfDay"]'):
        param.text = exit_eor
    for param in root.findall('.//Param[@key="EODExitTime"]'):
        param.text = eod_time


parser = argparse.ArgumentParser(description='Generador de Proyectos SQX')
parser.add_argument('--mm-type', type=str, choices=['1', '2'], help='Tipo de Money Management: 1=Fijo, 2=Riesgo %%')
parser.add_argument('--mm-value', type=str, help='Valor de lote o porcentaje de riesgo')
parser.add_argument('--limit-time', type=str, default='false', choices=['true', 'false'], help='Limitar rango de tiempo')
parser.add_argument('--time-from', type=str, default='0', help='Segundos desde la medianoche para inicio')
parser.add_argument('--time-to', type=str, default='0', help='Segundos desde la medianoche para fin')
parser.add_argument('--exit-eor', type=str, default='false', choices=['true', 'false'], help='Cerrar al final del rango / dia')
parser.add_argument('--eod-time', type=str, default='86100', help='Segundos desde la medianoche para cierre forzado')
args = parser.parse_args()

mm_type = args.mm_type
mm_value = args.mm_value

# Dynamic Time Limit Args (Handled directly via CLI/AI logic)
limit_time = args.limit_time
time_from = args.time_from
time_to = args.time_to
exit_eor = args.exit_eor
eod_time = args.eod_time

if not mm_type or not mm_value:
    print("=========================================================")
    print(" CONFIGURACION DE CUSTOM PROJECT")
    print("=========================================================")
    print("\n--- MONEY MANAGEMENT ---")
    print("1: Lote Fijo (Ej: 0.01) [Recomendado para Portafolio]")
    print("2: Riesgo Fijo % de Balance (Ej: 1, 2, 5) [Fondeo/Futuros]")
    
    try:
        if sys.stdin.isatty():
            if not mm_type:
                mm_type = input("Selecciona el tipo de MM (1 o 2) [Default 1]: ").strip() or "1"
            if not mm_value:
                if mm_type == "1":
                    val = input("Introduce el tamaño del lote [Default 0.01]: ").strip()
                    mm_value = val if val else "0.01"
                elif mm_type == "2":
                    val = input("Introduce el % de riesgo por operacion [Default 1]: ").strip()
                    mm_value = val if val else "1"
        else:
            print("Entorno no interactivo detectado. Usando defaults para MM.")
            if not mm_type: mm_type = "1"
            if not mm_value: mm_value = "0.01"
    except Exception as e:
        if not mm_type: mm_type = "1"
        if not mm_value: mm_value = "0.01"

if not mm_type: mm_type = "1"
if not mm_value: mm_value = "0.01"

print(f"\nGenerando proyecto con MM Tipo {mm_type} (Valor {mm_value})...")
if limit_time == 'true':
    print(f"Filtro de Tiempo Activo: Inicio {time_from}s, Fin {time_to}s. Cierre forzado EOD: {exit_eor} ({eod_time}s)")
print("\n")

shutil.copy(base_cfx, out_cfx)
temp_dir = 'temp_cfx_orb'
os.makedirs(temp_dir, exist_ok=True)

with zipfile.ZipFile(out_cfx, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

for root_dir, dirs, files in os.walk(temp_dir):
    for file in files:
        if file.endswith('.xml'):
            file_path = os.path.join(root_dir, file)
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            if file == 'Build-Task1.xml':
                for param in root.findall('.//Param[@key="ExitAtEndOfDay"]'):
                    # Ya no forzamos ExitAtEndOfDay aqui sin más, lo maneja configure_time_filters
                    pass
                for block in root.findall('.//BuildingBlocks/Block[@category="signals"]'):
                    block.set('use', 'false')
                blocks_parent = root.find('.//BuildingBlocks')
                if blocks_parent is not None:
                    ET.SubElement(blocks_parent, 'Block', {'key': 'ORBLongBreakout', 'weight': '1', 'use': 'true', 'category': 'signals'})
                    ET.SubElement(blocks_parent, 'Block', {'key': 'ORBShortBreakout', 'weight': '1', 'use': 'true', 'category': 'signals'})
                for block in root.findall('.//BuildingBlocks/Block[@key="Volume"]'): block.set('use', 'true')
                for block in root.findall('.//BuildingBlocks/Block[@key="ATR"]'): block.set('use', 'true')
                for block in root.findall('.//BuildingBlocks/Block[@key="SMA"]'): block.set('use', 'true')
                for block in root.findall('.//BuildingBlocks/Block[@key="EMA"]'): block.set('use', 'true')
            
            configure_money_management(root, mm_type, mm_value)
            configure_time_filters(root, limit_time, time_from, time_to, exit_eor, eod_time)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)

replacements = {
    '__TICK_SYMBOL__': 'GBPUSD', '__NORMAL_SYMBOL__': 'GBPUSD', '[[__ASSET__]]': 'GBPUSD', '__ASSET__': 'GBPUSD',
    'FX_XCCY_Currency1__BROKER_PROFILE__': 'No Session', '__SESSION__': 'No Session', '[__BROKER_PROFILE__]': 'Dukascopy',
    '__BROKER_PROFILE__': 'Dukascopy', '__BROKER_NAME__': 'Dukascopy', '__INSTRUMENT__': 'GBPUSD', '__BUILDER_START__': '2010.01.01',
    '__OOS_START__': '2023.01.01', '__TICK_START__': '2010.01.01', '__NORMAL_END__': '2026.01.01', '__TICK_END__': '2026.01.01',
    '__DATE_REPLACE__': '2010.01.01', 'key="ORBLongBreakout"': 'key="CBlock_ORBLongBreakout"', 'key="ORBShortBreakout"': 'key="CBlock_ORBShortBreakout"',
    'robCombRows="2"': 'robCombRows="3"', 'robCombCols="2"': 'robCombCols="3"', 'robMinComb="3"': 'robMinComb="9"'
}

for root_dir, dirs, files in os.walk(temp_dir):
    for file in files:
        if file.endswith('.xml'):
            file_path = os.path.join(root_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            for old_str, new_str in replacements.items():
                content = content.replace(old_str, new_str)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

with zipfile.ZipFile(out_cfx, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root_dir, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root_dir, file)
            arcname = os.path.relpath(file_path, temp_dir)
            zipf.write(file_path, arcname)

shutil.rmtree(temp_dir)
print(f'Project successfully updated at {out_cfx}')
