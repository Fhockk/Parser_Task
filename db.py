from db_settings import postgresql as settings
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData
from sqlalchemy_utils import database_exists, create_database


def get_engine(user, passwd, host, port, db):
    url = f'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, echo=False)
    return engine


engine = get_engine(settings['pguser'],
                    settings['pgpasswd'],
                    settings['pghost'],
                    settings['pgport'],
                    settings['pgdb'])

meta = MetaData()

ad_list = Table('Ad_list', meta,
                Column('id_ad', Integer, primary_key=True),
                Column('image', String(255)),
                Column('title', String(100)),
                Column('date', String(20)),
                Column('location', String(50)),
                Column('beds', String(50)),
                Column('description', String(255)),
                Column('price', Float(25)),
                Column('currency', String(5))
)

meta.create_all(engine)
