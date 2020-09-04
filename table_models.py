from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
# the variable base holds the class returned from declarative_base method, which is the parent for all the table classes
Base = declarative_base()


class ToDo(Base):
    __tablename__ = 'task'  # The table name
    # Table columns
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    # returns the string representation for a row in the table
    def __repr__(self):
        return f"{self.task}"
