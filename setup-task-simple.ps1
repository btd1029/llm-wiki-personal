# シンプル版: LLM Wiki Auto-Ingest スケジュール登録
$taskName = "LLM-Wiki-Auto-Ingest"
$taskPath = "\LLM-Wiki\"
$batchFile = "C:\Users\bitet\llm-wiki-personal\simple-ingest.bat"

# 既存タスクを削除
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "既存のタスクを削除しています..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Start-Sleep -Seconds 1
}

# トリガー: 5分ごと
$interval = New-TimeSpan -Minutes 5
$trigger = New-ScheduledTaskTrigger -RepetitionInterval $interval -RepetitionDuration (New-TimeSpan -Days 3650) -Once -At (Get-Date)

# アクション: バッチファイルを実行
$action = New-ScheduledTaskAction -Execute $batchFile

# 設定: 基本設定のみ
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

# タスクを登録
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -TaskPath $taskPath `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "LLM Wiki Auto-Ingest (5分ごと)" `
        -Force | Out-Null

    Write-Host "✅ タスク '$taskName' を正常に登録しました！" -ForegroundColor Green

    # 登録状況を確認
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($task) {
        Write-Host ""
        Write-Host "タスク情報:" -ForegroundColor Cyan
        Write-Host "  タスク名: $($task.TaskName)"
        Write-Host "  状態: $($task.State)"
        Write-Host "  説明: $($task.Description)"
    }
} catch {
    Write-Host "❌ エラーが発生しました:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}
