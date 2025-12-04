import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongodb():
    print("🔍 Тестирование подключения к MongoDB...")
    
    # Варианты подключения
    test_cases = [
        {
            "name": "Полный URL с базой",
            "url": "mongodb://localhost:27017/planner"
        },
        {
            "name": "URL без базы",
            "url": "mongodb://localhost:27017"
        },
        {
            "name": "Localhost с портом",
            "url": "localhost:27017"
        },
        {
            "name": "Только localhost",
            "url": "localhost"
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*50}")
        print(f"Тест: {test['name']}")
        print(f"URL: {test['url']}")
        
        try:
            # Пробуем подключиться
            client = AsyncIOMotorClient(test['url'], serverSelectionTimeoutMS=5000)
            
            # Проверяем подключение
            await client.admin.command('ping')
            print("✅ MongoDB доступна!")
            
            # Получаем информацию о сервере
            server_info = await client.server_info()
            print(f"   Версия MongoDB: {server_info.get('version', 'неизвестно')}")
            
            # Показываем доступные базы
            database_names = await client.list_database_names()
            print(f"   Доступные базы данных: {database_names}")
            
            # Проверяем базу planner
            if 'planner' in database_names:
                print("   ✅ База 'planner' существует")
                db = client.planner
                collections = await db.list_collection_names()
                print(f"   Коллекции в 'planner': {collections}")
            else:
                print("   ⚠️  База 'planner' не существует")
                print("   (Будет создана автоматически при первом обращении)")
            
            await client.close()
            
        except Exception as e:
            print(f"❌ Ошибка подключения: {type(e).__name__}")
            print(f"   Сообщение: {str(e)}")
    
    print(f"\n{'='*50}")
    print("📋 Итоговая рекомендация:")
    print("Используй в .env файле: DATABASE_URL=mongodb://localhost:27017/planner")

if __name__ == "__main__":
    # Проверяем, установлен ли motor
    try:
        import motor
        print("✅ Библиотека motor установлена")
    except ImportError:
        print("❌ Библиотека motor не установлена")
        print("Установите: pip install motor")
        sys.exit(1)
    
    # Запускаем тест
    asyncio.run(test_mongodb())
