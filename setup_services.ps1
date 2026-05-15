# Download Redis
Write-Host "Downloading Redis..."
Invoke-WebRequest -Uri "https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip" -OutFile "redis.zip"
Expand-Archive -Path "redis.zip" -DestinationPath "redis_bin" -Force
Remove-Item "redis.zip"

# Download PostgreSQL (15 is a safe choice, ~200MB)
Write-Host "Downloading PostgreSQL..."
Invoke-WebRequest -Uri "https://get.enterprisedb.com/postgresql/postgresql-15.8-1-windows-x64-binaries.zip" -OutFile "postgres.zip"
Expand-Archive -Path "postgres.zip" -DestinationPath "pg_bin" -Force
Remove-Item "postgres.zip"

Write-Host "Initializing PostgreSQL..."
$pg_path = ".\pg_bin\pgsql"
$data_dir = ".\pg_data"
if (-Not (Test-Path $data_dir)) {
    & "$pg_path\bin\initdb.exe" -D $data_dir -U postgres -A trust
}

Write-Host "Starting PostgreSQL..."
& "$pg_path\bin\pg_ctl.exe" -D $data_dir -l logfile start

Write-Host "Waiting for PostgreSQL to start..."
Start-Sleep -Seconds 3

Write-Host "Creating user and database..."
& "$pg_path\bin\psql.exe" -U postgres -c "CREATE USER test_user WITH PASSWORD 'test_password';"
& "$pg_path\bin\psql.exe" -U postgres -c "CREATE DATABASE core_auth_test OWNER test_user;"
& "$pg_path\bin\psql.exe" -U postgres -c "ALTER USER test_user WITH SUPERUSER;"

Write-Host "Starting Redis..."
Start-Process -FilePath ".\redis_bin\redis-server.exe" -WindowStyle Hidden

Write-Host "Services are up and running!"
