from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(url='sqlite:///projectdb1.db')
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

def session_factory():
    # Create database tables (if they don't exist)
    Base.metadata.create_all(engine)
    

if __name__ == "__main__":
    session_factory()
    print("Database created")