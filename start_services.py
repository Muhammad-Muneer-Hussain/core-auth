import os
import urllib.request
import zipfile
import subprocess
import time

def download_and_extract(url, zip_path, extract_to):
    if not os.path.exists(extract_to):
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, zip_path)
        print(f"Extracting to {extract_to}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_path)
    else:
        print(f"Already extracted to {extract_to}")

# Redis 5.0.14
redis_url = "https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip"
download_and_extract(redis_url, "redis.zip", "redis_bin")

# Postgres 15
pg_url = "https://get.enterprisedb.com/postgresql/postgresql-15.8-1-windows-x64-binaries.zip"
download_and_extract(pg_url, "postgres.zip", "pg_bin")

pg_path = os.path.join("pg_bin", "pgsql")
data_dir = "pg_data"

if not os.path.exists(data_dir):
    print("Initializing Postgres...")
    subprocess.run([os.path.join(pg_path, "bin", "initdb.exe"), "-D", data_dir, "-U", "postgres", "-A", "trust"], check=True)

print("Starting Postgres...")
subprocess.run([os.path.join(pg_path, "bin", "pg_ctl.exe"), "-D", data_dir, "-l", "logfile", "start"], check=True)

print("Waiting for Postgres to start...")
time.sleep(3)

print("Creating user and DB...")
subprocess.run([os.path.join(pg_path, "bin", "psql.exe"), "-U", "postgres", "-c", "CREATE USER test_user WITH PASSWORD 'test_password';"])
subprocess.run([os.path.join(pg_path, "bin", "psql.exe"), "-U", "postgres", "-c", "CREATE DATABASE core_auth_test OWNER test_user;"])
subprocess.run([os.path.join(pg_path, "bin", "psql.exe"), "-U", "postgres", "-c", "ALTER USER test_user WITH SUPERUSER;"])

print("Starting Redis...")
subprocess.Popen([os.path.join("redis_bin", "redis-server.exe")], creationflags=subprocess.CREATE_NO_WINDOW)

print("Services started successfully!")
