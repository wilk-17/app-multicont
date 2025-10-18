"""Safely insert Flasgger docstrings into API route handlers that lack them.

- Uses AST to find function defs with route decorators.
- Inserts a minimal docstring (responses $ref) after the def line with proper indentation.
- Creates a .bak backup for each modified file.
"""
from pathlib import Path
import ast
import re

API_DIR = Path('app') / 'api'

def infer_model_from_filename(stem):
    resource = stem[:-4] if stem.endswith('_api') else stem
    return ''.join(p.capitalize() for p in resource.split('_'))

changed_files = []
for file in sorted(API_DIR.glob('*_api.py')):
    src = file.read_text(encoding='utf-8')
    try:
        tree = ast.parse(src)
    except SyntaxError:
        print(f"Skipping {file}: syntax error")
        continue
    lines = src.splitlines()
    inserts = []  # (insert_at_line_index (0-based), docstring_lines)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            # check for decorators containing 'route'
            has_route = any(getattr(d, 'attr', '') == 'route' or getattr(d, 'func', None) is not None and getattr(getattr(d, 'func', 'attr'), 'attr', '') == 'route' for d in node.decorator_list)
            if not has_route:
                continue
            # skip if function already has docstring
            if ast.get_docstring(node) is not None:
                continue
            # infer model from file name
            model = infer_model_from_filename(file.stem)
            # determine if function appears to be item endpoint (has param 'id')
            arg_names = [a.arg for a in node.args.args]
            is_item = 'id' in arg_names
            # craft docstring
            if is_item:
                doc = [f'"""', f'{model} endpoint', '---', f'tags:', f'  - {model}', 'responses:', "  200:", f"    description: {model}", '    schema:', f"      $ref: '#/definitions/{model}'", '"""']
            else:
                doc = [f'"""', f'{model} list endpoint', '---', f'tags:', f'  - {model}', 'responses:', "  200:", '    description: Lista', '    schema:', '      type: array', '      items:', f"        $ref: '#/definitions/{model}'", '"""']
            # insert after def line
            def_line_idx = node.lineno - 1
            insert_at = def_line_idx + 1
            # compute indentation: take leading whitespace of the next line if present, else def indentation + 4
            if insert_at < len(lines):
                next_line = lines[insert_at]
                m = re.match(r"(\s*)", next_line)
                indent = m.group(1) if m else ''
            else:
                # fallback
                m = re.match(r"(\s*)", lines[def_line_idx])
                indent = (m.group(1) if m else '') + '    '
            # ensure docstring lines are indented properly
            doc_lines = [(indent + l) if l.strip() != '' else l for l in doc]
            inserts.append((insert_at, doc_lines))
    if not inserts:
        print(f'No changes for {file.name}')
        continue
    # apply inserts in reverse order (so indexes remain valid)
    new_lines = list(lines)
    for idx, doc_lines in sorted(inserts, key=lambda x: x[0], reverse=True):
        new_lines[idx:idx] = doc_lines + ['']
    bak = file.with_suffix(file.suffix + '.bak')
    file.rename(bak)
    file.write_text('\n'.join(new_lines), encoding='utf-8')
    changed_files.append((file.name, str(bak)))
    print(f'Updated {file.name} (backup: {bak.name})')

print('Done. Modified files:', changed_files)
