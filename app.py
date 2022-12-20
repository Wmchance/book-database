# import models
from models import Base, Book, session, engine
# main menu - add, search, analysis, exit, view
# add books to the db
# edit books
# search books 
# delete books 
# data cleaning 
# loop runs the project

if __name__ == '__main__':
    Base.metadata.create_all(engine)