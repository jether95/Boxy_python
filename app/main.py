from typing import List

from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import schemas, Client, User, Category
#from Category import Category as categoryModel
from .Database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

Category.Base.metadata.create_all(bind=engine)
Client.Base.metadata.create_all(bind=engine)
User.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://127.0.0.1:8000/ ",
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def getDb():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#Metodos GET
@app.get("/")
async def main():
    return RedirectResponse(url="/docs")

@app.get('/category', response_model=List[schemas.Category])
def showCategory(db:Session=Depends(getDb)):
    categories = db.query(Category.Category).all()
    return categories

@app.get('/client', response_model=List[schemas.Client])
def showClient(db:Session=Depends(getDb)):
    clients = db.query(Client.Client).all()
    return clients

@app.get('/user', response_model=List[schemas.User])
async def showUser(db: Session = Depends(getDb)):
    users = db.query(User.User).all()
    return users

#Metodos POST
@app.post('/category/',response_model=schemas.Category)
def createCategory (entrada: schemas.Category, db: Session=Depends(getDb)):
    category = Category.Category(id=entrada.id, nombre=entrada.nombre)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

