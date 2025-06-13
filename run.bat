@echo off

start cmd /k "cd /d %~dp0 && call env\Scripts\activate && python server.py"

timeout /t 15

start cmd /k "c:\Python27\python.exe test.py"
