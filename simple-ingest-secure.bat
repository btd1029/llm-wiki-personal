@echo off
REM LLM Wiki Auto-Ingest バッチファイル（セキュア版）
REM ANTHROPIC_API_KEY環境変数が設定されていることを前提とします

chcp 65001 > nul
cd C:\Users\bitet\llm-wiki-personal

REM 環境変数が設定されているかチェック
if not defined ANTHROPIC_API_KEY (
    echo [%date% %time%] エラー: ANTHROPIC_API_KEY が設定されていません
    exit /b 1
)

set PYTHONIOENCODING=utf-8

echo [%date% %time%] Ingest開始

for %%F in (raw\*.md) do (
    if not "%%F"=="raw\.gitkeep" (
        echo 処理中: %%F
        python personal-ingest.py --source "%%F"
    )
)

echo [%date% %time%] Ingest完了
