from sqlalchemy import create_engine  # create_engine method to create the db file
from sqlalchemy.orm import sessionmaker  # To create a session object to manage the db
from datetime import datetime, timedelta
import sys
from table_models import ToDo, Base


engine = create_engine('sqlite:///todo.db?check_same_thread=False') # created the database
Base.metadata.create_all(engine)  # create all the tables in the database

Session = sessionmaker(bind=engine)
session = Session()  # created a session object to manage the db


def print_rows(rows, mode=0):
    counter = 1
    for row in rows:
        if not mode:
            print(f'{counter}. {row}. ')
        else:
            print(f'{counter}. {row}. {row.deadline.day} {row.deadline.strftime("%b")} {row.deadline.year}')
        counter += 1
        


def day_tasks(day=datetime.today()):
    rows = session.query(ToDo).filter(ToDo.deadline == day.date()).all()
    if len(rows) < 1:
        print('Nothing to do!')
    else:
        print_rows(rows)


def today_tasks(day):
    print(f"Today {day.day} {day.strftime('%b')}:")
    day_tasks(day)


def week_tasks(day):
    for i in range(0, 7):
        week_day = (day + timedelta(i))
        print(f"{week_day.strftime('%A')} {week_day.day} {week_day.strftime('%b')}")
        day_tasks(week_day)
        print()


def all_tasks():
    print('All tasks:')
    rows = session.query(ToDo).order_by(ToDo.deadline).all()
    if len(rows) < 1:
        print('Nothing to do!')
    else:
        print_rows(rows, 1)


def add_task():
    task = input('Enter Task\n')
    string_date = input('Enter deadline on the form "YYYY-MM-DD" or "MM-DD"\n')
    try:
        date = [int(value) for value in string_date.split('-')]  # The deadline should be YYYY-MM-DD
        if len(date) < 3:
            date.insert(0, datetime.today().year)  # Consider the current year as the default year
        deadline = datetime(date[0], date[1], date[2])
    except:
        print('Invalid date or date format for deadline')
        return None
    if deadline.date() >= datetime.today().date():    
        new_row = ToDo(task=task, deadline=deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!')
    else:
        print("The task will only be added if the specified deadline is in the future!")
        return None



def missed_tasks(day):
    rows = session.query(ToDo).filter(ToDo.deadline < day.date()).order_by(ToDo.deadline).all()
    print('Missed tasks:')
    if len(rows) < 1:
        print('Nothing is missed!')
    else:
        print_rows(rows, 1)


def delete_task():
    rows = session.query(ToDo).order_by(ToDo.deadline).all()
    if len(rows) < 1:
        print('Nothing to delete!')
    else:
        print('Choose the number of the task you want to delete:')
        print_rows(rows, 1)
        task_id = int(input('0. Cancel\n'))
        if task_id == 0: return None
        delete_row = rows[task_id - 1]
        session.delete(delete_row)
        session.commit()
        print('The task has been deleted!')


while True:
    entry = input('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
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
        missed_tasks(today)

    elif entry == '5':
        add_task()

    elif entry == '6':
        delete_task()

    elif entry == '0':
        print('Bye!')
        session.close()
        sys.exit(0)
    else:
        print('Invalid entry!')
        continue

session.close()
