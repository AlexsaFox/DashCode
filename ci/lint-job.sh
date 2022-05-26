#!/bin/bash
cd api
echo "Entered directory"
source venv/bin/activate
echo "Sourced venv"
which python
which pip
black --check . --config=pyproject.toml
isort --check .
mypy --config-file=pyproject.toml
