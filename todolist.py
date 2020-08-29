from sqlalchemy import create_engine, Column, Integer, String, Date  # create_engine method to create the db file
from sqlalchemy.ext.declarative import declarative_base  # to return a Base parent class to all the Table classes
from datetime import datetime
from sqlalchemy.orm import sessionmaker  # To create a session object to manage the db
import sys

Base = declarative_base()  # created the Base parent class


# A model class for a table in the data base
class ToDo(Base):
    __tablename__ = 'task'  # The table name
    # Table columns
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    # returns the string representation for a row in the table
    def __repr__(self):
        return f"{self.id}. {self.task}"


engine = create_engine('sqlite:///todo.db?check_same_thread=False') # created the database
Base.metadata.create_all(engine)  # create all the tables in the database

Session = sessionmaker(bind=engine)
session = Session()  # created a session object to manage the db
while True:
    print('''
1) Today's tasks
2) Add task
0) Exit''')
    entry = input()
    # Check the entry in the menu
    if entry == '1':
        rows = session.query(ToDo).all()
        print('Today: ')
        if len(rows) < 1:
            print('Nothing to do!')
            continue
        else:
            for row in rows:
                print(row)
    elif entry == '2':
        print('Enter task')
        task = input()
        new_row = ToDo(task=task)
        session.add(new_row)
        session.commit()
    elif entry == '0':
        print('Bye!')
        sys.exit(0)
    else:
        print('Invalid entry!')
        continue



