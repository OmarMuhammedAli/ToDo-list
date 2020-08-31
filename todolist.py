from sqlalchemy import create_engine, Column, Integer, String, Date  # create_engine method to create the db file
from sqlalchemy.ext.declarative import declarative_base  # to return a Base parent class to all the Table classes
from datetime import datetime, timedelta
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
        return f"{self.task}"


engine = create_engine('sqlite:///todo.db?check_same_thread=False') # created the database
Base.metadata.create_all(engine)  # create all the tables in the database

Session = sessionmaker(bind=engine)
session = Session()  # created a session object to manage the db


def day_tasks(day=datetime.today()):
    rows = session.query(ToDo).filter(ToDo.deadline == day.date()).all()
    if len(rows) < 1:
        print('Nothing to do!')
    else:
        counter = 1
        for row in rows:
            print(f'{counter}. {row}')
            counter += 1


def today_tasks(day):
    print(f"Today {today.day} {today.strftime('%b')}:")
    day_tasks(today)


def week_tasks(day):
    for i in range(0, 7):
        week_day = (today + timedelta(i))
        print(f"{week_day.strftime('%A')} {week_day.day} {week_day.strftime('%b')}")
        day_tasks(week_day)
        print()


def all_tasks():
    print('All tasks:')
    rows = session.query(ToDo).order_by(ToDo.deadline).all()
    if len(rows) < 1:
        print('Nothing to do!')
    else:
        for row in rows:
            print(f'{row.id}. {row}. {row.deadline.day} {row.deadline.strftime("%b")}')


def add_task():
    task = input('Enter Task\n')
    date = [int(value) for value in input('Enter deadline\n').split('-')]  # The deadline should be YYYY-MM-DD
    new_row = ToDo(task=task, deadline=datetime(date[0], date[1], date[2]))
    session.add(new_row)
    session.commit()
    print('The task has been added!')


while True:
    entry = input('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Add task
0) Exit
''')
    today = datetime.today()
    # Check the entry in the menu
    if entry == '1':
        today_tasks(today)

    elif entry == '2':
        week_tasks(today)

    elif entry == '3':
        all_tasks()

    elif entry == '4':
        add_task()

    elif entry == '0':
        print('Bye!')
        session.close()
        sys.exit(0)
    else:
        print('Invalid entry!')
        continue

session.close()
