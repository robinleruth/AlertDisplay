#!/bin/bash

echo "Create virtual env"

python -m venv venv

source venv/bin/activate

echo "Install requirements"

python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Launch GUI"
python gui.py
