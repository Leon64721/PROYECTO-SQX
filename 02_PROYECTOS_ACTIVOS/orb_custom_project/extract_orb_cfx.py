import zipfile, os

project_path = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\ORB_MTF_Project.cfx'
extract_dir = r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\temp_orb_cfx'

os.makedirs(extract_dir, exist_ok=True)

try:
    with zipfile.ZipFile(project_path, 'r') as z:
        z.extractall(extract_dir)
    print(f"Successfully extracted {project_path} to {extract_dir}")
except FileNotFoundError:
    print(f"Error: The file {project_path} was not found.")
except zipfile.BadZipFile:
    print(f"Error: {project_path} is not a valid zip file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
