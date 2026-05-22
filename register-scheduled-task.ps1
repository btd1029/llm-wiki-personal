# LLM Wiki Auto-Ingest スケジュール登録スクリプト
# Windows Task Scheduler に定期実行タスクを登録

$TaskName = "LLM-Wiki-Auto-Ingest"
$TaskPath = "\LLM-Wiki\"
$FullTaskPath = $TaskPath + $TaskName
$BatchFile = "C:\Users\bitet\llm-wiki-personal\simple-ingest.bat"

# 既存タスクを削除（ある場合）
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "既存のタスク '$TaskName' を削除しています..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Start-Sleep -Seconds 1
}

# トリガー設定: 5分ごと
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365 * 10) -Once -At (Get-Date)

# アクション設定: バッチファイルを実行
$action = New-ScheduledTaskAction -Execute $BatchFile

# 設定: 起動できない場合は次回の実行時に実行
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBattery -StartWhenAvailable

# プリンシパル設定: 現在のユーザーで実行
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# タスクを登録
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -TaskPath $TaskPath `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Principal $principal `
        -Description "LLM Wiki: raw フォルダを監視して自動で要約生成（5分ごと）" `
        -Force

    Write-Host "✅ タスク '$TaskName' を登録しました！" -ForegroundColor Green
    Write-Host ""
    Write-Host "タスク詳細:" -ForegroundColor Cyan
    Write-Host "  実行ファイル: $BatchFile"
    Write-Host "  実行間隔: 5分ごと"
    Write-Host "  説明: LLM Wiki: raw フォルダを監視して自動で要約生成"
    Write-Host ""

    # 登録されたタスクを確認
    $task = Get-ScheduledTask -TaskName $TaskName
    Write-Host "登録状態:" -ForegroundColor Cyan
    Write-Host "  タスク名: $($task.TaskName)"
    Write-Host "  状態: $($task.State)"

} catch {
    Write-Host "❌ エラーが発生しました:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}
