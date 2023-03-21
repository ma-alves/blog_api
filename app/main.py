# SELECIONAR O INTERPRETADOR DO VENV
# run on terminal 'venv\Scripts\activate.bat'
# tanto o interpretador quanto o terminal devem ser configurados para os do venv
# run: uvicorn app.main:app --reload

from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import mysql.connector
from time import sleep
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    # validation class
    title: str
    content: str
    published: bool = True # optional field


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


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # armazena novamente os dados commitados para que possam ser retonados no return
    return {'data':new_post}


@app.get('/posts/{id}')
def get_posts_id(id: int):
    cursor.execute('SELECT * FROM posts WHERE id = %s', (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return {'data': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    deleted = cursor.fetchone()
    conn.commit()
    if deleted == None:
        pass
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='index not found.')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_posts(id: int, post: Post):
    cursor.execute('UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        pass
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='index not found.')
    return {'updated_data': updated_post}
