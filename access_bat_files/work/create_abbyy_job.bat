@echo off
@cd C:\Users\913678186\IdeaProjects\RemediationTests\access_bat_files\work
@C:\Users\913678186\IdeaProjects\RemediationTests\venv\Scripts\python.exe create_abbyy_job.py %1 %2
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on

::C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files\run_pdf_accessibility_check.bat
::C:\Users\913678186\IdeaProjects\RemediationTests\access_bat_files\run_pdf_accessibility_check.bat