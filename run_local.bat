@echo off

REM Create necessary directories
if not exist backend\logs mkdir backend\logs

REM Install dependencies
pip install -r requirements.txt

REM Start the server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 