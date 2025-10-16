@echo off
setlocal enableextensions enabledelayedexpansion

IF NOT EXIST .venv (
  python -m venv .venv
)
CALL .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
