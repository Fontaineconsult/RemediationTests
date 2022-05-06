@echo off
@cd C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files
@C:\Users\DanielPC\Desktop\Servers\RemediationTests\root\windowsvenv\Scripts\python.exe finalize_pdf_file_conversion.py %1
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on

::C:\Users\DanielPC\Desktop\Servers\RemediationTests\venv\Scripts\access_bat_files\finalize_pdf_file_conversion.bat