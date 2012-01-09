import sys
sys.path.append("..")
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from lib.models import Model

Base = declarative_base()
engine = create_engine('sqlite:///../db/cams.db', convert_unicode=True)
Base.metadata.create_all(engine)