from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import Integer, String, DateTime, Float, ARRAY
import pandas as pd
import config

aws_params = {
    'host': config.db_host,
    'database': config.database,
    'port': config.port,
    'user': config.username,
    'password': config.password
}

url = URL.create(
    drivername = 'postgresql',
    username = aws_params['user'],
    host = aws_params['host'],
    database = aws_params['database'],
    password = aws_params['password'],
    port = aws_params['port']
)

engine = create_engine(url)

metadata = MetaData()

genre_table = Table('genres',
                    metadata,
                    Column('id', Integer, primary_key = True),
                    Column('created_at', DateTime),
                    Column('name', String),
                    Column('slug', String),
                    Column('updated_at', DateTime),
                    Column('url', String),
                    Column('checksum', String))

# create table 'games' in database
game_titles = Table('games',
                    metadata,
                    Column('id', Integer),
                    Column('first_release_date', DateTime),
                    Column('follows', Integer),
                    Column('genres', ARRAY(Integer)),
                    Column('keywords', ARRAY(Integer)),
                    Column('name', String),
                    Column('rating', Float),
                    Column('rating_count', Integer),
                    Column('slug', String),
                    Column('tags', ARRAY(Integer)),
                    Column('total_rating', Float),
                    Column('url', String),
                    Column('themes', ARRAY(Integer)),
                    Column('aggregated_rating', Float)
                    )

metadata.create_all(engine)