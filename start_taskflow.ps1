# Get the current directory where the script is located
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Set Python path (modify this if needed)
$pythonPath = "python"

# Start Flask app
Write-Host "Starting Flask application..."
$process = Start-Process -FilePath $pythonPath -ArgumentList "app.py" -PassThru -NoNewWindow

# Wait a moment
Start-Sleep -Seconds 5

# Check if the process is running
if ($process.HasExited) {
    Write-Host "Failed to start Flask application"
    exit
}

# Try to open the browser
Write-Host "Opening browser..."
Start-Process "http://127.0.0.1:5000"

# Keep the window open
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Clean up
Stop-Process -Id $process.Id -Force