@echo off

:LOOP

coverage run "%~dp0\videoserver\test.py"
coverage html

pause
goto LOOP
