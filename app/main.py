# SELECIONAR O INTERPRETADOR DO VENV
# run on terminal 'venv\Scripts\activate.bat'
# tanto o interpretador quanto o terminal devem ser configurados para os do venv
# run: uvicorn app.main:app --reload

from typing import List
from fastapi import FastAPI, status, HTTPException, Response, Depends
import mysql.connector
from time import sleep
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {'message':'welcome to my api!!!'}

