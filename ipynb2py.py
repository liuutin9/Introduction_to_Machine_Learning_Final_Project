import sys
import json

def ipynb2py(ipynb_file, py_file):
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        ipynbDict = json.load(f)
    lines = []
    for cell in ipynbDict['cells']:
        if cell['cell_type'] == 'code':
            lines += cell['source']
            lines.append('\n\n')
        elif cell['cell_type'] == 'markdown':
            lines.append("'''\n")
            lines += cell['source']
            lines.append("\n'''\n\n")
    with open(py_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
    print(f'{ipynb_file} -> {py_file}')
    
if __name__ == '__main__':
    ipynb2py(sys.argv[1], sys.argv[2])