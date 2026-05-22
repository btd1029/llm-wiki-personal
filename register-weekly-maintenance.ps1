# Register wiki-maintenance.py to run weekly
$taskName = "LLM-Wiki-Weekly-Maintenance"
$taskPath = "\LLM-Wiki\"
$pythonScript = "C:\Users\bitet\llm-wiki-personal\wiki-maintenance.py"
$workingDir = "C:\Users\bitet\llm-wiki-personal"

# Check if Python script exists
if (-not (Test-Path $pythonScript)) {
    Write-Host "ERROR: wiki-maintenance.py not found at $pythonScript"
    exit 1
}

# Delete existing task if present
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Deleting existing task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Start-Sleep -Seconds 1
}

# Create trigger: Every Sunday at 10:00 AM
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "10:00:00"
Write-Host "Created trigger: Weekly on Sunday at 10:00 AM"

# Create action: Run Python script
# Note: Update ANTHROPIC_API_KEY in environment variables first
$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument "$pythonScript" `
    -WorkingDirectory $workingDir

# Create settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

# Register task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -TaskPath $taskPath `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Karpathy-style Wiki Maintenance - Index & Backlinks" `
        -Force | Out-Null

    Write-Host "✓ Task registered successfully"

    # Verify
    $task = Get-ScheduledTask -TaskName $taskName
    Write-Host ""
    Write-Host "Task Details:"
    Write-Host "  Name: $($task.TaskName)"
    Write-Host "  Path: $($task.TaskPath)"
    Write-Host "  State: $($task.State)"
    Write-Host "  Trigger: Weekly Sunday at 10:00 AM"
    Write-Host ""
    Write-Host "Next Run: Check Task Scheduler"
    Write-Host ""
    Write-Host "✅ Setup Complete!"
} catch {
    Write-Host "ERROR: Failed to register task"
    Write-Host $_.Exception.Message
    exit 1
}
