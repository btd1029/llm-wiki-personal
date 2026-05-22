$taskName = "LLM-Wiki-Auto-Ingest"
$taskPath = "\LLM-Wiki\"
$batchFile = "C:\Users\bitet\llm-wiki-personal\simple-ingest.bat"

$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Start-Sleep -Seconds 1
}

$interval = New-TimeSpan -Minutes 5
$trigger = New-ScheduledTaskTrigger -RepetitionInterval $interval -RepetitionDuration (New-TimeSpan -Days 3650) -Once -At (Get-Date)

$action = New-ScheduledTaskAction -Execute $batchFile

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Action $action -Trigger $trigger -Settings $settings -Description "LLM Wiki Auto-Ingest" -Force | Out-Null

$task = Get-ScheduledTask -TaskName $taskName
Write-Host "Success: Task registered"
Write-Host "Name: $($task.TaskName)"
Write-Host "State: $($task.State)"
