import os

def search_text():
    for r, d, files in os.walk('temp_cfx_search'):
        for f in files:
            try:
                with open(os.path.join(r, f), 'r', encoding='utf-8', errors='ignore') as file:
                    if 'Cloned' in file.read():
                        print(f'Found Cloned in {os.path.join(r, f)}')
            except Exception as e:
                pass

search_text()