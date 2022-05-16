#!/bin/bash
ls -la
cd api
ls -la
echo "Init venv"
python -m venv venv
echo "Inited venv"
source venv/bin/activate
echo "Sourced venv"
which python
which pip
pip install --upgrade pip 
pip install -qr requirements.txt
pip uninstall psycopg2-binary asyncpg -y -q
pip install --no-binary :all: psycopg2 asyncpg
echo "Installed requirements.txt"