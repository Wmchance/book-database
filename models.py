from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///books.db', echo = False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    published_date = Column(Date)
    price = Column(Integer)

    def __repr__(self) -> str:
        return super().__repr__()

# create a db
    #books.db
# create a model
    # Needs: Title, Author, Date Published, & price