from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # armazena novamente os dados commitados para que possam ser retonados no return
    return new_post


@router.get('/{id}', response_model=schemas.Post)
def get_posts_id(id: int, db: Session = Depends(get_db)):
    one_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    
    return one_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    query_to_del = db.query(models.Post).filter(models.Post.id == id)

    if query_to_del.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='index not found.')
    
    query_to_del.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    query_to_upd = db.query(models.Post).filter(models.Post.id == id)

    if query_to_upd.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='index not found.')
    
    query_to_upd.update(post.dict(), synchronize_session=False)
    db.commit()
    return query_to_upd.first()
