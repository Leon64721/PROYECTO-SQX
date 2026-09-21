import os
import sys

sys.path.insert(0, r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-strategy-project\engine')
from generate import make_project, deploy

def main():
    install = r"C:\SQX_144_Full"
    base_folder = "Builder"
    template_set = "NDXm_Fleet"
    new_name = "NDXm_NY_Session_Project"
    
    base_project_path = os.path.join(install, "user", "projects", base_folder, "project.cfx")
    template_path = os.path.join(install, "user", "settings", "StrategyTemplates", template_set, "NDXm_NY_Session_Template.sqx")
    
    tasks = [{
        "template": template_path,
        "output_db": "NDXm_NY_Session"
    }]
    
    out_dir = r"E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\out"
    os.makedirs(out_dir, exist_ok=True)
    
    out_cfx = os.path.join(out_dir, f"{new_name}.cfx")
    cfx = make_project(base_project_path, new_name, tasks, out_cfx=out_cfx)
    print("Project built successfully:", cfx)
    
    # Deploy
    deploy(out_cfx, install, new_name)
    print("Deployed project to SQX.")

if __name__ == '__main__':
    main()