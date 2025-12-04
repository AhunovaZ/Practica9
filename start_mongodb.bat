@echo off
echo Запуск MongoDB 8.2...
echo.
echo Проверяем наличие MongoDB...
if not exist "C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe" (
    echo ❌ MongoDB 8.2 не найдена по пути
    dir "C:\Program Files\MongoDB\Server\"
    pause
    exit /b 1
)

echo ✅ MongoDB найдена
echo Запускаем MongoDB...
echo.
echo Не закрывай это окно! Оно должно оставаться открытым.
echo.
cd "C:\Program Files\MongoDB\Server\8.2\bin"
mongod --dbpath C:\mongodb_data
pause
