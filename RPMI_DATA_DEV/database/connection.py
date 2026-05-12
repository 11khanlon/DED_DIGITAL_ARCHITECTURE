'''
Responsible for schema creation 
ingestion 
SQL inserts 
engine connection 

'''

from sqlalchemy import create_engine
import pandas as pd
import uuid
import sys
import numpy as np


DB_USER = "postgres"
DB_PASSWORD = "pushtostart"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "am_cdm"

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

print("PostgreSQL engine created.")


