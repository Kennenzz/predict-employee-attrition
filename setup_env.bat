@echo off
echo ==============================
echo   SETUP DATA ANALYST PROJECT
echo ==============================

REM 1. Kiem tra Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Loi: Python chua duoc cai dat. Vui long cai Python 3.10+ truoc.
    pause
    exit /b
)

REM 2. Tao moi truong ao (neu chua co)
if not exist venv (
    echo Tao moi truong ao (venv)...
    python -m venv venv
) else (
    echo Moi truong ao da ton tai. Bo qua buoc tao.
)

REM 3. Kich hoat moi truong ao
call venv\Scripts\activate

REM 4. Cap nhat pip
echo Cap nhat pip...
python -m pip install --upgrade pip

REM 5. Cai thu vien tu requirements.txt (neu co)
if exist requirements.txt (
    echo Cai thu vien tu requirements.txt...
    pip install -r requirements.txt
) else (
    echo Khong tim thay file requirements.txt, bo qua.
)

echo ==============================
echo Setup hoan tat !
echo Moi truong ao da duoc kich hoat.
echo Ban co the chay:
echo    jupyter notebook
echo hoac mo VS Code de lam viec.
echo ==============================
pause
