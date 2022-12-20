# import models
from models import Base, Book, session, engine

import datetime
import csv

# main menu - add, search, analysis, exit, view
def menu():
    print('''
    \n1. Add book
    \r2. View book
    \r3. Search for a book
    \r4. Book analysis
    \r5. Exit''')
    while True:
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above
            \rA number from 1-5
            \rPress enter to choose again''')

# add books to the db
# edit books
# search books 
# delete books 
# data cleaning & import from CSV
def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    month = int(months.index(split_date[0])+1)
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)

def clean_price(price_str):
    price_float = float(price_str)
    return int(price_float * 100)    

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()

# loop runs the project
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1': 
            #add book
            title = input('Title: ')
            author = input('Author: ')
            date = input('Published date (Ex: October 25, 2017): ')
            date_clean = clean_date(date)
            price = input('Price (Ex: 25.88): ')
            price_clean = clean_price(price)
        elif choice == '2':
            #view book
            pass
        elif choice == '3':
            #search book
            pass
        elif choice == '4':
            #analysis
            pass
        else:
            print('Goodbye')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()