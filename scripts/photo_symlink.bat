@echo off

REM Check if plink is available
where plink >nul 2>nul
if %errorlevel% neq 0 (
    echo plink is not installed or not in PATH.
    exit /b 1
)

REM Prompt user for temporary directory
set /p "temporary_dir=Enter temporary directory: "

REM Prompt user for source directory
set /p "source_dir=Enter source directory path: "

REM Prompt user for destination directory
set /p "destination_dir=Enter destination directory path: "

REM Prompt user for password
set /p "password=Enter root password: "

REM Replace {alexandria_IP} placeholders with actual IP address or hostname
set /p "alexandria_IP=Enter Alexandria server IP: "

REM Execute the shell script remotely using plink
plink -ssh root@%alexandria_IP% -pw %password% "/mnt/user/DevRack/DevRack/scripts/photo_symlink.sh %temporary_dir% %source_dir% %destination_dir%"
