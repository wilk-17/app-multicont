"""Generate discrepancy report using AST/regex parsing (no imports).

This script extracts field names from entity/model files by finding assignments
like `name = db.Column(...)`. It also scans use_cases for attribute usage and
API files for $ref definitions and request parameters.

Outputs:
 - reports/discrepancy_ast.json
 - reports/discrepancy_ast.md
"""
from pathlib import Path
import re
import json

ROOT = Path('.')
APP = ROOT / 'app'
ENTITIES = APP / 'entities'
MODELS = APP / 'models'
APIS = APP / 'api'
USE_CASES = APP / 'use_cases'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)

def extract_columns_from_file(path: Path):
    text = path.read_text(encoding='utf-8')
    cols = []
    # simplistic: find lines like "name = db.Column(" (strip spaces)
    for m in re.finditer(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*db\.Column\(", text, re.M):
        cols.append(m.group(1))
    return cols

entity_fields = {}
for p in sorted(ENTITIES.glob('*.py')):
    cls_name = p.stem.capitalize()
    cols = extract_columns_from_file(p)
    # try to detect actual class name in file
    text = p.read_text(encoding='utf-8')
    class_match = re.search(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text)
    if class_match:
        cls_name = class_match.group(1)
    entity_fields[cls_name] = cols

model_fields = {}
for p in sorted(MODELS.glob('*.py')):
    cls_name = p.stem.capitalize()
    cols = extract_columns_from_file(p)
    text = p.read_text(encoding='utf-8')
    class_match = re.search(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text)
    if class_match:
        cls_name = class_match.group(1)
    model_fields[cls_name] = cols

handler_fields = {}
for p in sorted(USE_CASES.glob('*_handler.py')):
    text = p.read_text(encoding='utf-8')
    names = set()
    for m in re.finditer(r"\.filter_by\(([^)]*)\)", text):
        inside = m.group(1)
        parts = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", inside)
        for part in parts:
            names.add(part)
    for m in re.finditer(r"\w+\.([a-zA-Z_][a-zA-Z0-9_]*)\s*=" , text):
        names.add(m.group(1))
    handler_fields[p.stem] = sorted(names)

api_refs = {}
for p in sorted(APIS.glob('*_api.py')):
    text = p.read_text(encoding='utf-8')
    refs = set()
    params = set()
    for m in re.finditer(r"\$ref:\s*'#/definitions/([A-Za-z0-9_]+)'", text):
        refs.add(m.group(1))
    for m in re.finditer(r"request\.args\.get\(\s*['\"]([a-zA-Z0-9_]+)['\"]", text):
        params.add(m.group(1))
    api_refs[p.stem] = {
        'refs': sorted(refs),
        'params': sorted(params)
    }

# Build report
models = set(list(entity_fields.keys()) + list(model_fields.keys()))
report = {}
for model in sorted(models):
    ent = entity_fields.get(model, [])
    legacy = model_fields.get(model, [])
    apis_using = [k for k,v in api_refs.items() if model in v.get('refs', [])]
    handlers_using = [k for k,v in handler_fields.items() if any(col in v for col in ent)]
    report[model] = {
        'entity_fields': ent,
        'legacy_model_fields': legacy,
        'api_files_referencing': apis_using,
        'handler_files_candidate': handlers_using
    }

(REPORTS / 'discrepancy_ast.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

md = ['# Discrepancy AST Report', '']
for m,info in report.items():
    md.append(f'## {m}')
    md.append(f"- entity_fields: {info['entity_fields']}")
    md.append(f"- legacy_model_fields: {info['legacy_model_fields']}")
    md.append(f"- api_files_referencing: {info['api_files_referencing']}")
    md.append(f"- handler_files_candidate: {info['handler_files_candidate']}")
    md.append('')

(REPORTS / 'discrepancy_ast.md').write_text('\n'.join(md), encoding='utf-8')
print('AST-based report generated: reports/discrepancy_ast.json and reports/discrepancy_ast.md')
