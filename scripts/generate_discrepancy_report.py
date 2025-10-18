"""Generate discrepancy report between entities, legacy models, API docstrings, and handlers.

Output:
 - reports/discrepancy.json
 - reports/discrepancy.md

Fields extracted:
 - For entities/models: column names from SQLAlchemy model (.__table__.columns)
 - For use_cases handlers: attributes accessed via hasattr in code (best-effort) and assignments to attributes
 - For API files: parameters and fields referenced in to_dict() (best-effort)

This is a heuristic tool; it will report best-effort matches and missing items.
"""
import ast
import json
from pathlib import Path
import re
import importlib.util
import sys

ROOT = Path('.')
APP = ROOT / 'app'
ENTITIES = APP / 'entities'
MODELS = APP / 'models'
APIS = APP / 'api'
USE_CASES = APP / 'use_cases'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)

report = {}

# Helper to safely import a module from a path

def import_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)  # type: ignore
        return mod
    except Exception:
        return None

# 1) collect entity fields using runtime import (sa meta)
entity_fields = {}
for p in sorted(ENTITIES.glob('*.py')):
    name = p.stem
    mod = import_module_from_path(p)
    if not mod:
        continue
    # find class in module that inherits db.Model by checking for __table__
    for obj_name in dir(mod):
        obj = getattr(mod, obj_name)
        if hasattr(obj, '__table__'):
            try:
                cols = [c.name for c in obj.__table__.columns]
                entity_fields[obj_name] = cols
            except Exception:
                continue

# 2) collect legacy model fields similarly
model_fields = {}
for p in sorted(MODELS.glob('*.py')):
    name = p.stem
    mod = import_module_from_path(p)
    if not mod:
        continue
    for obj_name in dir(mod):
        obj = getattr(mod, obj_name)
        if hasattr(obj, '__table__'):
            try:
                cols = [c.name for c in obj.__table__.columns]
                model_fields[obj_name] = cols
            except Exception:
                continue

# 3) analyze use_cases handlers (best effort: look for Model.query or .filter_by references and attribute sets)
handler_fields = {}
for p in sorted(USE_CASES.glob('*_handler.py')):
    text = p.read_text(encoding='utf-8')
    # find pattern Model.query.filter_by(x= or .filter(Model.x == )
    names = set()
    for m in re.finditer(r"\.filter_by\(([^)]*)\)", text):
        inside = m.group(1)
        parts = re.findall(r"(\w+)\s*=", inside)
        for part in parts:
            names.add(part)
    # attribute assignments like obj.field =
    for m in re.finditer(r"\w+\.([a-zA-Z_][a-zA-Z0-9_]*)\s*=" , text):
        names.add(m.group(1))
    handler_fields[p.stem] = sorted(names)

# 4) analyze API files: try to find to_dict properties and parameters
api_fields = {}
for p in sorted(APIS.glob('*_api.py')):
    text = p.read_text(encoding='utf-8')
    names = set()
    # look for item.to_dict() usage, try to find keys in to_dict implementations (best-effort: check corresponding entity)
    # parse parameters from route docstrings - look for $ref or schema keys
    for m in re.finditer(r"\$ref: '#/definitions/([A-Za-z0-9_]+)'", text):
        names.add(f"ref:{m.group(1)}")
    # find request.args.get('field'
    for m in re.finditer(r"request\.args\.get\(\s*['\"]([a-zA-Z0-9_]+)['\"]", text):
        names.add(m.group(1))
    api_fields[p.stem] = sorted(names)

# Build model-centric report
models = set(list(entity_fields.keys()) + list(model_fields.keys()))
for model in sorted(models):
    ent = entity_fields.get(model, [])
    legacy = model_fields.get(model, [])
    # find api references to model name
    api_refs = [k for k,v in api_fields.items() for ref in v if ref == f"ref:{model}"]
    handlers = [k for k,v in handler_fields.items() if model.lower().startswith(k.replace('_handler','').split('_')[0]) or any(col in v for col in ent)]
    report[model] = {
        'entity_fields': ent,
        'legacy_model_fields': legacy,
        'api_files_referencing': api_refs,
        'handler_files_candidate': handlers,
    }

# also include entities that are in definitions but not in entities (if any)
# write JSON and Markdown
(REPORTS / 'discrepancy.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

md_lines = ["# Discrepancy Report\n"]
for model, info in report.items():
    md_lines.append(f"## {model}\n")
    md_lines.append(f"- Entity fields: {info['entity_fields']}\n")
    md_lines.append(f"- Legacy model fields: {info['legacy_model_fields']}\n")
    md_lines.append(f"- API files referencing model: {info['api_files_referencing']}\n")
    md_lines.append(f"- Candidate handler files: {info['handler_files_candidate']}\n")

(REPORTS / 'discrepancy.md').write_text('\n'.join(md_lines), encoding='utf-8')
print('Report generated at reports/discrepancy.json and reports/discrepancy.md')
