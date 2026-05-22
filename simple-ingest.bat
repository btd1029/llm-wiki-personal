@echo off
chcp 65001 > nul
cd C:\Users\bitet\llm-wiki-personal
set PYTHONIOENCODING=utf-8

REM Read ANTHROPIC_API_KEY from environment variable
if not defined ANTHROPIC_API_KEY (
    echo ERROR: ANTHROPIC_API_KEY environment variable is not set
    echo Please set it using PowerShell Admin:
    echo [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-xxx", "User")
    exit /b 1
)

echo Processing started...
for %%F in (raw\*.md) do (
    if not "%%F"=="raw\.gitkeep" (
        echo Processing file: %%F
        python personal-ingest.py --source "%%F"
    )
)
echo Processing completed.
