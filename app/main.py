# SELECIONAR O INTERPRETADOR DO VENV
# run on terminal 'venv\Scripts\activate.bat'
# tanto o interpretador quanto o terminal devem ser configurados para os do venv
# run: uvicorn app.main:app --reload

from typing import List
from fastapi import FastAPI, status, HTTPException, Response, Depends
import mysql.connector
from time import sleep
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='#senai0308',
            database='blogapi'
        )
        cursor = conn.cursor(dictionary=True)
        break
    except mysql.Error as e:
        print(e)
        sleep(10)


@app.get('/')
def root():
    return {'message':'welcome to my api!!!'}


@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # armazena novamente os dados commitados para que possam ser retonados no return
    return new_post


@app.get('/posts/{id}', response_model=schemas.Post)
def get_posts_id(id: int, db: Session = Depends(get_db)):
    one_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    
    return one_post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    query_to_del = db.query(models.Post).filter(models.Post.id == id)

    if query_to_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='index not found.')
    
    query_to_del.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    query_to_upd = db.query(models.Post).filter(models.Post.id == id)

    if query_to_upd.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='index not found.')
    
    query_to_upd.update(post.dict(), synchronize_session=False)
    db.commit()
    return query_to_upd.first()


@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
