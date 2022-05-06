@echo off
@cd C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files
@C:\Users\DanielPC\Desktop\Servers\RemediationTests\root\windowsvenv\Scripts\python.exe run_pdf_accessibility_check.py %1 %2
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on

::C:\Users\913678186\IdeaProjects\RemediationTests\access_bat_files\run_pdf_accessibility_check.bat
::C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files\run_pdf_accessibility_check.bat
::@IF %ERRORLEVEL% NEQ 0 PAUSE

