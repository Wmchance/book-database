# import models
from models import Base, Book, session, engine

import datetime
import csv
import time

# main menu - add, search, analysis, exit, view
def menu():
    while True:
        print('''
            \nProgramming Books Tool
            \r1. Add book
            \r2. View book
            \r3. Search for a book
            \r4. Book analysis
            \r5. Exit
            ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above
            \rA number from 1-5
            \rPress enter to choose again
            ''')


def submenu():
    while True:
        print('''
            \n1. Edit
            \r2. Delete
            \r3. Return to main menu
            ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above
            \rA number from 1-3
            \rPress enter to choose again''')

def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0])+1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n**** Date Error ****
        \rThe date format should be: MONTH DD, YYYY & in the past
        \rEx: March 22, 1965
        \rPress Enter to try again
        \r********************''')
        return
    else: 
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
        \n**** Price Error ****
        \rThe date format should only include: dollars & cents separated with a period
        \rEx: 24.56
        \rPress Enter to try again
        \r********************''')
        return
    else:
        return int(price_float * 100)    


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n**** ID Error ****
        \rThe book id must be a number from one of the provided options
        \rPress Enter to try again
        \r********************''')
        return
    else:
        if book_id in options:
            return book_id
        else: 
            input(f'''
            \n**** ID Error ****
            \rThe book id must be a number from the following list:
            \r{options}
            \rPress Enter to try again
            \r********************''')
            return


def edit_check(column_name, current_value):
    print(f'\n*** Edit {column_name} ***')
    if column_name == 'price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'published_date':
        print(f'Current Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'Current Value: {current_value}')

    if column_name == 'published_date' or column_name == 'price':
        while True:
            changes = input('\nWhat would you like to change the value to? ')
            if column_name == 'published_date':
                changes = clean_date(changes)
                if type(changes) == datetime.date: 
                    return changes
            elif column_name == 'price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else: 
        return input('\nWhat would you like to change the value to? ')


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
        #add book
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 25.88): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print(f"'{title}' added")
            time.sleep(1.5)
        #view all books
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress Enter to return to the main menu')
        #search for a book
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                \nId options: {id_options}
                \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == id_choice).first()
            print(f'''
            \n{the_book.title} by {the_book.author}
            \rPublished: {the_book.published_date}
            \rPrice: ${the_book.price / 100}\n''')
            sub_choice = submenu()
            #Edit book values
            if sub_choice == '1':
                the_book.title = edit_check('title', the_book.title)
                the_book.author = edit_check('author', the_book.author)
                the_book.published_date = edit_check('published_date', the_book.published_date)
                the_book.price = edit_check('price', the_book.price)
                session.commit()
                print('Book updated')
                time.sleep(1.5 )
            #Delete the book
            elif sub_choice == '2': 
                session.delete(the_book)
                session.commit()
                print('Book deleted')
                time.sleep(1.5 )
        #Analysis of book
        elif choice == '4':
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%Python%')).count()
            print(f'''
                \n**** Book Analysis ****
                \rOldest Book: {oldest_book}
                \rNewest Book: {newest_book}
                \rTotal Books: {total_books}
                \rPython Books: {python_books}
            ''')
            input('\nPress Enter to return to the main menu')
        else:
            print('Goodbye')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()