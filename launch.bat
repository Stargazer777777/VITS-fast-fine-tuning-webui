call venv\scripts\activate.bat

set PATH=%PATH%./win_bin;

@REM uvicorn server.main:app --reload --host 192.168.1.3 --port 7777