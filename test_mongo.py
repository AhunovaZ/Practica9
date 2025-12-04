# test_mongo.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def test():
    try:
        client = AsyncIOMotorClient('mongodb://localhost:27017')
        # Получаем информацию о сервере
        info = await client.server_info()
        print("MongoDB работает!")
        print(f"Версия: {info['version']}")

        # Проверим базу данных planner
        db = client.planner
        collections = await db.list_collection_names()
        print(f"База данных 'planner': {collections}")

        await client.close()
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test())
    if success:
        print("\nВсё готово для продолжения практики!")
    else:
        print("\nНужно установить motor библиотеку")
        print("Выполни: pip install motor")