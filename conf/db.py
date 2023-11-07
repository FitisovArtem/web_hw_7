import configparser
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_conf = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

conf = configparser.ConfigParser()
conf.read(file_conf)

user = conf.get('DEV_DB', 'USER')
password = conf.get('DEV_DB', 'PASSWORD')
domain = conf.get('DEV_DB', 'DOMAIN')
port = conf.get('DEV_DB', 'PORT')
db = conf.get('DEV_DB', 'DB_NAME')

URI = f'postgresql://{user}:{password}@{domain}:{port}/{db}'

engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)

DBSession = sessionmaker(bind=engine)
session = DBSession()
