from datetime import datetime, timedelta
import sys
from functions import *

while True:
    entry = input('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
7) Move deadline
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

    elif entry == '7':
        move_deadline()

    elif entry == '0':
        print('Bye!')
        session.close()
        sys.exit(0)

    else:
        print('Invalid entry!')

session.close()
