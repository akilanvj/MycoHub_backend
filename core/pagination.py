from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9000",  # Example: frontend running on different port
    "http://127.0.0.1:9000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=List[ItemResponse])
def read_items(start: int = 0, limit: int = 10, name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Item)
    if name:
        query = query.filter(Item.name.contains(name))
    items = query.offset(start).limit(limit).all()
    return items
