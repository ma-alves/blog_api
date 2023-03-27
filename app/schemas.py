from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    # validation class
    title: str
    content: str
    published: bool = True # optional field

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
