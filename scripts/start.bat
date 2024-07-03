@echo off
title VisorView
cd ..

rem Read the contents of PYTHON_PATH into %PYTHON_PATH%:
set /P PYTHON_PATH=<PYTHON_PATH

%PYTHON_PATH% -m main
pause