from fastapi import FastAPI
from database.connection_fixed import Settings
import routes.events
import routes.users

app = FastAPI()

# Инициализация настроек
settings = Settings()

# Подключение маршрутов
app.include_router(routes.events.event_router, prefix="/event")
app.include_router(routes.users.user_router, prefix="/user")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()
    print("✅ База данных инициализирована")

@app.get("/")
async def home():
    return {"message": "Welcome to the Event Planner API with MongoDB!"}

@app.get("/health")
async def health():
    return {"status": "ok", "database": "MongoDB"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
