from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import uvicorn

# ========== Модели ==========
class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[str]] = []

    class Settings:
        name = "users"

# Pydantic модели для запросов
class EventCreate(BaseModel):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ========== FastAPI ==========
app = FastAPI()

# ========== Инициализация БД ==========
@app.on_event("startup")
async def startup():
    print("🚀 Запуск Event Planner API...")
    
    try:
        # Подключаемся к MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017/planner")
        
        # Проверяем подключение
        await client.admin.command('ping')
        print("✅ MongoDB подключена!")
        
        # Инициализируем Beanie
        await init_beanie(
            database=client.planner,
            document_models=[Event, User]
        )
        print("✅ Beanie инициализирован")
        
        app.mongodb = client
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Проверь что MongoDB запущена!")

# ========== Роуты ==========
@app.get("/")
async def root():
    return {"message": "Event Planner API с MongoDB"}

@app.get("/health")
async def health():
    return {"status": "ok", "database": "MongoDB"}

# ========== События (CRUD) ==========
@app.get("/events")
async def get_events():
    events = await Event.find_all().to_list()
    return events

@app.post("/events")
async def create_event(event: EventCreate):
    new_event = Event(**event.dict())
    await new_event.create()
    return {"message": "Event created", "id": str(new_event.id)}

@app.get("/events/{id}")
async def get_event(id: str):
    from beanie import PydanticObjectId
    try:
        event = await Event.get(PydanticObjectId(id))
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except:
        raise HTTPException(status_code=404, detail="Event not found")

@app.put("/events/{id}")
async def update_event(id: str, event_update: EventUpdate):
    from beanie import PydanticObjectId
    try:
        event = await Event.get(PydanticObjectId(id))
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Обновляем только переданные поля
        update_data = event_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event, key, value)
        
        await event.save()
        return {"message": "Event updated", "event": event}
    except:
        raise HTTPException(status_code=404, detail="Event not found")

@app.delete("/events/{id}")
async def delete_event(id: str):
    from beanie import PydanticObjectId
    try:
        event = await Event.get(PydanticObjectId(id))
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        await event.delete()
        return {"message": "Event deleted"}
    except:
        raise HTTPException(status_code=404, detail="Event not found")

# ========== Пользователи ==========
@app.post("/users/signup")
async def signup(user: UserCreate):
    # Проверяем уникальность email
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(**user.dict())
    await new_user.create()
    return {"message": "User created"}

@app.post("/users/login")
async def login(credentials: UserLogin):
    user = await User.find_one(User.email == credentials.email)
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

# ========== Запуск ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🎯 Event Planner API с MongoDB (Полный CRUD)")
    print("📡 Сервер запускается на http://localhost:8080")
    print("📚 Документация: http://localhost:8080/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)
