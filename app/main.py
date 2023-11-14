from typing import List

from fastapi import FastAPI, Depends, Request, HTTPException
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import schemas
from .Models import Category, User, Client
#from Category import Category as categoryModel
from .Database import SessionLocal, engine
from .jwt_manager import create_token, validate_token
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

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

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['user'] != "juaco":
            raise HTTPException(status_code=403, detail="Credenciales incorrectas")



#Metodos GET
@app.get("/")
async def main():
    return RedirectResponse(url="/docs")

@app.get('/category', response_model=List[schemas.Category], dependencies=[Depends(JWTBearer())])
def showCategory(db:Session=Depends(getDb)):
    categories = db.query(Category.Category).all()
    return categories

#Cliente
@app.get('/client', response_model=List[schemas.Client])
def showClient(db:Session=Depends(getDb)):
    clients = db.query(Client.Client).all()
    return clients

@app.post('/client/', response_model=schemas.Client)
def createClient(schema: schemas.Client, dataBase: Session=Depends(getDb)):
    cliente = Client.Client(name=schema.name, lastName=schema.lastName, document=schema.document)
    dataBase.add(cliente)
    dataBase.commit()
    dataBase.refresh(cliente)
    return cliente

@app.put('/cliente/{client_id}', response_model=schemas.Client)
def updateClient(client_id: int, schema: schemas.Client, dataBase: Session = Depends((getDb))):
    client = dataBase.query(Client.Client).filter_by(Id=client_id).first()
    client.name = schema.name
    client.lastName = schema.lastName
    client.document = schema.document
    dataBase.commit()
    dataBase.refresh(client)
    return client

@app.delete('/client/{client_id}', response_model=schemas.Client)
def deleteClient(client_id: int, schema: schemas.Client, dataBase: Session=Depends(getDb)):
    client = dataBase.query(Client.Client).filter_by(Id=client_id).first()
    dataBase.delete(client)
    dataBase.commit()
    respuesta = schemas.Respuesta(mensaje=f'Cliente {client_id} eliminado correctamente')
    return client

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

@app.put('/category/{category_id}',response_model=schemas.Category)
def UpdateCategory (category_id: int, entrada: schemas.CategoryUpdate, db: Session=Depends(getDb)):
    category = db.query(Category.Category).filter_by(id = category_id).first()
    category.nombre = entrada.nombre
    db.commit()
    db.refresh(category)
    return category

@app.delete('/category/{category_id}',response_model=schemas.Respuesta)
def DeleteCategory (category_id: int, db: Session=Depends(getDb)):
    category = db.query(Category.Category).filter_by(id = category_id).first()
    db.delete(category)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta

@app.post('/login', tags=['auth'])
def login(user: schemas.User):
    if user.id == 1 and user.user == "juaco" and user.password == "123":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)
