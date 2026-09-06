from backend.app.core.config import settings


from sqlalchemy import create_engine
engine = create_engine(settings.database_url, echo=False)  # echo=True)


from sqlalchemy.orm import DeclarativeBase, sessionmaker
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass


def get_db():
    db=SessionLocal()

    try :
        yield db
    finally :
        db.close()



