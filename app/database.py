from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:#senai0308@127.0.0.1/blogapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # engine responsável por conectar a URL do db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # cria sessão, responsável por 'falar' com o db

Base = declarative_base() # instância responsável por criar modelos em models.py

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        