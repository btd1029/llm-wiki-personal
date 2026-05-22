@echo off
REM Execute PowerShell script to setup scheduled task
setlocal enabledelayedexpansion
cd /d C:\Users\bitet\llm-wiki-personal

powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\setup-task.ps1'"
pause
