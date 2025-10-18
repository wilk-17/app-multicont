@echo off
call venv\Scripts\activate.bat
set FLASK_APP=run.py
set FLASK_ENV=development
python run.py
