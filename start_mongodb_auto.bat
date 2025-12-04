@echo off
echo Поиск MongoDB...
echo.

set MONGO_PATH=

REM Проверяем разные версии
if exist "C:\Program Files\MongoDB\Server\8.2.2\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\8.2.2\bin
)
if exist "C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\8.2\bin
)
if exist "C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\8.0\bin
)
if exist "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\7.0\bin
)
if exist "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" (
    set MONGO_PATH=C:\Program Files\MongoDB\Server\6.0\bin
)

if "%MONGO_PATH%"=="" (
    echo ❌ MongoDB не найдена!
    echo Проверь установку MongoDB
    dir "C:\Program Files\MongoDB\Server\"
    pause
    exit /b 1
)

echo Найдена MongoDB в: %MONGO_PATH%
echo Запускаем...

cd "%MONGO_PATH%"
mongod --dbpath C:\mongodb_data
pause
