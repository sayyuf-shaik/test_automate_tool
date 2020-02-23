import pony.orm as pny
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.actions import Tests, Table


def fetch_tables():
    with pny.db_session:
        table_names = pny.select(i.name for i in Table)
        list_of_tables = table_names.fetch()
        return list_of_tables
