@echo off
call venv\Scripts\activate.bat
set FLASK_APP=run.py
flask db migrate -m "Align models with database schema"
