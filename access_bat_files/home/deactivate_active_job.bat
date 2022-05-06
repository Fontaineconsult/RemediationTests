@echo off
@cd C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files
@C:\Users\DanielPC\Desktop\Servers\RemediationTests\root\windowsvenv\Scripts\python.exe deactivate_active_job.py %1
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on