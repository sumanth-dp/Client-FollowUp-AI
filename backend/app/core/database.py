from backend.app.core.config import settings


from sqlalchemy import create_engine
engine = create_engine(settings.database_url, echo=True)


from sqlalchemy.orm import DeclarativeBase, sessionmaker
SessionLocal = sessionmaker(binf=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass


def get_db():
    db=SessionLocal()

    try :
        yield db
    finally :
        db.close()



