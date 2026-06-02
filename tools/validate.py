#!/usr/bin/env python3
import json
from pathlib import Path
import sys

try:
    import yaml
    import jsonschema
except ImportError as exc:
    print(f'Missing dependency: {exc.name}', file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'schemas' / 'course.schema.json').read_text())

errors = []
for path in (ROOT / 'courses').glob('CRS-*/course.yaml'):
    data = yaml.safe_load(path.read_text())
    try:
        jsonschema.validate(data, SCHEMA)
    except jsonschema.ValidationError as exc:
        errors.append(f'{path}: {exc.message}')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)

print('Validation passed')
