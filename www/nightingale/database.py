import os
from sqlalchemy import create_engine

dbpath = os.path.join(os.path.dirname(__file__), 'data.db')
db = create_engine('sqlite:///' + dbpath)

def drop_database():
    if os.path.exists(dbpath):
        os.unlink(dbpath)
    
def create_database():
    path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    schema = open(path).read()
    result = [db.execute(line) for line in schema.split(';')]
