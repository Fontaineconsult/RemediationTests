@echo off
@cd C:\Users\913678186\IdeaProjects\RemediationTests\access_bat_files\work
@C:\Users\913678186\IdeaProjects\RemediationTests\venv\Scripts\python.exe PdfRepair.py %1 %2
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on

::C:\Users\DanielPC\Desktop\Servers\RemediationTests\venv\Scripts\access_bat_files\finalize_pdf_file_conversion.bat