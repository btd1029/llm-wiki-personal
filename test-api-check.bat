@echo off
set PYTHONIOENCODING=utf-8
if not defined ANTHROPIC_API_KEY (
    echo ERROR: ANTHROPIC_API_KEY is not set
    exit /b 1
)
echo SUCCESS: API key is defined
echo API Key starts with: %ANTHROPIC_API_KEY:~0,20%...
