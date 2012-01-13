import os
from sqlalchemy import create_engine

db = create_engine('sqlite:///data.db')

def drop_database():
    if os.path.exists('data.db'):
        os.unlink('data.db')
    
def create_database():
    path = os.path.join(os.path.dirname(__file__), '../schema.sql')
    schema = open(path).read()
    result = [db.execute(line) for line in schema.split(';')]
