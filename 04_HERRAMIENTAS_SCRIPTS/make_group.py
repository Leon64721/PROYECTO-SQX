import sys
sys.path.append(r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\.claude\skills\sqx-random-group')

from engine.groups import load_templates, inline_item, make_group, wrap_groups

def main():
    T = load_templates(r'C:\SQX_144_Full\internal\web\SQWIZARD\branding\global\config.xml')
    
    # We build a Value group (e.g. basic price levels or periods)
    items = [
        inline_item(T['Close']),
        inline_item(T['Open']),
        inline_item(T['High']),
        inline_item(T['Low']),
        inline_item(T['Highest']),
        inline_item(T['Lowest'])
    ]
    
    group_xml = make_group("Basic_Price_Levels", "Value", items, category="Levels")
    xml_content = wrap_groups([group_xml])
        
    with open(r'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\out\MTF_Value_Group.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    print("Created MTF_Value_Group.xml in out/")

if __name__ == '__main__':
    main()