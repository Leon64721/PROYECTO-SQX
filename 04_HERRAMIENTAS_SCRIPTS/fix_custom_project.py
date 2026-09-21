import zipfile
import xml.etree.ElementTree as ET
import os
import shutil

def fix_all_charts_in_cfx(cfx_path, out_path):
    print(f"Reparando: {cfx_path}")
    temp_dir = 'temp_repair_charts'
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(cfx_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
        
    build_xml_path = os.path.join(temp_dir, 'Build-Task1.xml')
    if not os.path.exists(build_xml_path):
        print("No se encontrÃ³ Build-Task1.xml")
        return
        
    # Obtener los Setups del Builder
    tree_b = ET.parse(build_xml_path)
    root_b = tree_b.getroot()
    setups_b = root_b.find('.//Data/Setups')
    
    if setups_b is None:
        print("No se encontrÃ³ la configuraciÃ³n Data/Setups en Builder")
        return
        
    # Aplicar a todos los Retest Tasks
    import glob
    retest_files = glob.glob(os.path.join(temp_dir, 'Retest-Task*.xml'))
    
    for rt_file in retest_files:
        tree_rt = ET.parse(rt_file)
        root_rt = tree_rt.getroot()
        
        # Reemplazar Data/Setups principal
        data_rt = root_rt.find('.//Data')
        if data_rt is not None:
            old_setups = data_rt.find('Setups')
            if old_setups is not None:
                # Modificamos los charts para asegurar que son identicos al builder, 
                # pero conservamos el Setup original de retest por las fechas
                setup_b_charts = setups_b.find('Setup').findall('Chart')
                setup_rt = old_setups.find('Setup')
                
                # Eliminar charts existentes
                for c in setup_rt.findall('Chart'):
                    setup_rt.remove(c)
                
                # Insertar los del builder (M30, M15, etc)
                for i, chart in enumerate(setup_b_charts):
                    # Copiamos el elemento para no tener problemas de referencia cruzada
                    import copy
                    new_chart = copy.deepcopy(chart)
                    setup_rt.insert(i, new_chart)
                    
        # Reemplazar CrossChecks Setups si existen
        cc_setups = root_rt.find('.//CrossChecks/RetestOnAdditionalMarkets/Settings/Setups')
        if cc_setups is not None:
            cc_setup = cc_setups.find('Setup')
            if cc_setup is not None:
                for c in cc_setup.findall('Chart'):
                    cc_setup.remove(c)
                for i, chart in enumerate(setup_b_charts):
                    import copy
                    new_chart = copy.deepcopy(chart)
                    cc_setup.insert(i, new_chart)
                    
        tree_rt.write(rt_file, encoding='utf-8', xml_declaration=True)
        print(f"Actualizado {os.path.basename(rt_file)} con los charts del Builder.")
            
    # Recomprimir
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root_dir, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    print(f"Ã‰xito: Archivo CFX reparado y guardado en {out_path}.")
    
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    base_cfx = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517\07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx'
    out_cfx = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517\07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY_FIXED.cfx'
    fix_all_charts_in_cfx(base_cfx, out_cfx)
