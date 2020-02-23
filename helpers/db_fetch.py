import pony.orm as pny
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.actions import Tests, Table


with pny.db_session:
    table_names = pny.select(i.name for i in Table)
    table_names.show()
    tables = table_names.fetch()
    print(tables)
    # print(tables.filter(lambda c: c))
    test_01_02 = pny.select(i for i in Tests if i.table_name == Table[2])
    test_01_02.show()
    # test_exec_01_02_04_05 = Table.select(name="Test_exec_01_02_04_05")

    # test_01_02_04 = Table.get(name="Test_exec_01_02_04")

    print('The Values of Test Execution test_01_02')
    for record in test_01_02:
        # print(record.title, record.description, record.test_id)
        # var = record.tests
        titles = record.title
        description = record.description
        print('titles = ', titles)
        print('description = ', description)

    """print('The Values of Test Execution test_01_02_04')
    for record in test_01_02_04.tests:
        print(record.title, record.description, record.test_id)"""

    """print('The Values of Test Execution Test_exec_01_02_04_05')
    for record in test_exec_01_02_04_05.tests:
        print(record.title, record.description, record.test_id)"""
    # update a record
    # band_name = Artist.get(name="Kutless")
    # band_name.name = "Beach Boys"
