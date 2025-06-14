@echo off
setlocal

start cmd /k "cd /d %~dp0 && call env\Scripts\activate && python server.py"

timeout /t 10

start cmd /k "c:\Python27\python.exe pc-test.py"

timeout /t 2

start cmd /k "cd /d %~dp0 && call env\Scripts\activate && python cam-emotion.py"
