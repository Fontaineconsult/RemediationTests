@echo off
@cd C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files
@C:\Users\DanielPC\Desktop\Servers\RemediationTests\root\windowsvenv\Scripts\python.exe replace_file_with_abbyy_file.py "%~1" "%~2"
@IF %ERRORLEVEL% NEQ 0 PAUSE
@echo on


::C:\Users\DanielPC\Desktop\Servers\RemediationTests\access_bat_files\replace_file_with_abbyy_file.bat
::C:\Users\913678186\IdeaProjects\RemediationTests\access_bat_files