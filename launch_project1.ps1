#run Docker on local machine
Write-Host "=== 1) Starting Docker Desktop ==="
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
Start-Sleep 35   # wait for Docker to fully start

#Docker Compose reads YAML file
Write-Host "=== 2) Starting Kafka containers ==="
cd C:\kafka-docker
docker compose up -d

Write-Host "Waiting for Kafka to become HEALTHY..."

#check Kafka health
$MAX_RETRIES = 30          # ~30 x 5s = 150 seconds max
$RETRY_COUNT = 0

while ($true) {

    $status = docker inspect `
        --format='{{.State.Health.Status}}' `
        kafka 2>$null

    if ($status -eq "healthy") {
        Write-Host "Kafka is healthy!"
        break
    }

    $RETRY_COUNT++

    if ($RETRY_COUNT -ge $MAX_RETRIES) {             # if kafka does not become healthy in time, start sleep
        Write-Host "Kafka did not become healthy in time."  
        Write-Host "Please check Docker logs."
        exit 1
    }

    Write-Host "Kafka status: $status (retry $RETRY_COUNT/$MAX_RETRIES)"
    Start-Sleep 5
}

#open VS Code folder
Write-Host "=== 3) Opening VS Code ==="
code "C:\kafka-docker"
Start-Sleep 3

#open powershell tab with fraud producer and consumer
Write-Host "=== 4) Launching Split-Screen Windows Terminal ==="

wt --% new-tab -p PowerShell -d "C:\kafka-docker\solutions" cmd /k "python fraud_consumer_kafka.py" ; split-pane -V -d "C:\kafka-docker\solutions" cmd /k "python auto_producer_kafka.py"
