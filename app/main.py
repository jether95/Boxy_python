from typing import List

from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import schemas, Category
from .Database import SessionLocal, engine

Category.Base.metadata.create_all(bind=engine)

app = FastAPI()

def getDb():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs")

@app.get('/category', response_model=List[schemas.Category])
def showCategory(db:Session=Depends(getDb)):
    categories = db.query(Category.Category).all()
    return categories