"""Add Flasgger docstrings referencing definitions for API endpoints.

This script scans `app/api/*.py`, infers a model name from the filename
(e.g. `inventory_item_api.py` -> `InventoryItem`) and inserts a minimal
YAML Flasgger docstring into route handler functions that currently lack one.

It creates a `.bak` copy before changing a file.

Run: python scripts/add_swagger_refs.py
"""
from pathlib import Path
import re

API_DIR = Path('app') / 'api'

route_re = re.compile(r"@[^\n]*route\(([^)]*)\)")
def_re = re.compile(r"def\s+(\w+)\s*\(")

for file in sorted(API_DIR.glob('*_api.py')):
    text = file.read_text(encoding='utf-8')
    lines = text.splitlines()
    changed = False
    out_lines = []
    i = 0
    # infer model name from filename
    stem = file.stem
    resource = stem[:-4] if stem.endswith('_api') else stem
    model = ''.join(p.capitalize() for p in resource.split('_'))
    # plural tag
    tag = model

    while i < len(lines):
        line = lines[i]
        out_lines.append(line)
        if line.strip().startswith('@') and 'route' in line:
            # capture decorator block (could be multiple decorators)
            dec_lines = [line]
            j = i + 1
            # include additional decorators above def
            while j < len(lines) and lines[j].strip().startswith('@'):
                dec_lines.append(lines[j])
                out_lines.append(lines[j])
                j += 1
            # expect def next
            if j < len(lines) and lines[j].strip().startswith('def '):
                def_line = lines[j]
                func_name = def_re.match(def_line.strip()).group(1)
                # check if function already has a docstring (triple quotes) in next non-empty line
                k = j + 1
                while k < len(lines) and lines[k].strip() == '':
                    k += 1
                has_doc = False
                if k < len(lines) and lines[k].strip().startswith(('"""', "'''")):
                    has_doc = True
                if not has_doc:
                    # parse route arg to determine if it's list or item
                    route_arg = dec_lines[-1]
                    # crude extraction of string literal inside route(...)
                    m = re.search(r"route\((.*)\)", route_arg)
                    path = ''
                    if m:
                        args = m.group(1)
                        s = re.search(r"(['\"]).*?\1", args)
                        if s:
                            path = s.group(0).strip("\"'")
                    # determine response schema
                    is_item = bool(re.search(r"<.*id.*>|\{id\}|\{\w+:id\}|\{\w+\}", path))
                    is_list = path.endswith('/') or path.endswith(')/') or path.endswith("'")
                    # craft docstring
                    if is_item:
                        schema_block = f"""responses:\n      200:\n        description: Objeto {model}\n        schema:\n          $ref: '#/definitions/{model}'\n"""
                    else:
                        schema_block = f"""responses:\n      200:\n        description: Lista de {model}\n        schema:\n          type: array\n          items:\n            $ref: '#/definitions/{model}'\n"""
                    yaml = [f'    """', f'    {model} endpoint', '    ---', f'    tags:', f'      - {tag}', '    parameters: []', '    ' + schema_block.strip().replace('\n', '\n    '), '    """']
                    # insert yaml after def line
                    out_lines.append(def_line)
                    out_lines.extend(yaml)
                    changed = True
                    # skip adding original def later
                    i = j
                else:
                    # no changes; def will be appended in normal flow
                    pass
        i += 1
    if changed:
        bak = file.with_suffix(file.suffix + '.bak')
        file.rename(bak)
        file.write_text('\n'.join(out_lines), encoding='utf-8')
        print(f'Updated {file} (backup at {bak})')
    else:
        print(f'No changes for {file}')
print('Done')
