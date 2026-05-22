# Register LLM Wiki Auto-Ingest scheduled task
$taskName = "LLM-Wiki-Auto-Ingest"
$taskPath = "\LLM-Wiki\"
$batchFile = "C:\Users\bitet\llm-wiki-personal\simple-ingest.bat"

# Remove existing task if present
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "古いタスクを削除しました"
}

# Create trigger - runs every 5 minutes
$at = Get-Date
$duration = New-TimeSpan -Days 3650
$interval = New-TimeSpan -Minutes 5

$trigger = New-ScheduledTaskTrigger -RepetitionInterval $interval -RepetitionDuration $duration -Once -At $at

# Create action
$action = New-ScheduledTaskAction -Execute $batchFile

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBattery -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath $taskPath `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "LLM Wiki Auto-Ingest (5分ごと実行)" `
    -Force | Out-Null

Write-Host "✅ タスク '$taskName' を登録しました"
Get-ScheduledTask -TaskName $taskName | Select-Object TaskName, State, Description
