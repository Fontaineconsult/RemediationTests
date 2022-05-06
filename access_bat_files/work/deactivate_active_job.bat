@echo off
@cd C:\Users\913678186\IdeaProjects\RemediationTests\access_bat_files\work
@C:\Users\913678186\IdeaProjects\RemediationTests\venvScripts\python.exe deactivate_active_job.py %1
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on