#!/bin/bash
# Execute from project root directory: `./scripts/publish.sh`

rm -rf dist
python -m build
twine upload dist/*
