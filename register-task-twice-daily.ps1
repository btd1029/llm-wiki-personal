$taskName = "LLM-Wiki-Auto-Ingest"
$taskPath = "\LLM-Wiki\"
$batchFile = "C:\Users\bitet\llm-wiki-personal\simple-ingest.bat"

# 既存タスクを削除
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Start-Sleep -Seconds 1
}

# トリガー1: 毎日朝8時
$trigger1 = New-ScheduledTaskTrigger -Daily -At "08:00:00"

# トリガー2: 毎日夜20時
$trigger2 = New-ScheduledTaskTrigger -Daily -At "20:00:00"

# アクション
$action = New-ScheduledTaskAction -Execute $batchFile

# 設定
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

# タスク登録（最初のトリガーで登録）
Register-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Action $action -Trigger $trigger1 -Settings $settings -Description "LLM Wiki Auto-Ingest (08:00 and 20:00)" -Force | Out-Null

# 2番目のトリガーを追加
$task = Get-ScheduledTask -TaskName $taskName
$task.Triggers += $trigger2
Set-ScheduledTask -InputObject $task

# 確認
$task = Get-ScheduledTask -TaskName $taskName
Write-Host "Success: Task registered"
Write-Host "Name: $($task.TaskName)"
Write-Host "State: $($task.State)"
Write-Host "Triggers:"
foreach ($trigger in $task.Triggers) {
    if ($trigger.StartBoundary) {
        Write-Host "  - Daily at $($trigger.StartBoundary.Split('T')[1])"
    }
}
