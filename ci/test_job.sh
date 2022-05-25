#!/bin/bash

ls -la
cd api
rm -rf .pytest_cache
source venv/bin/activate
pip uninstall psycopg2 -y
pip install psycopg2
pytest -c pyproject.toml --junitxml=report.xml
