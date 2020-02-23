import datetime
import pony.orm as pny

from helpers.db_create import Table, Tests


# ------------------------------------------------------------------------------
@pny.db_session
def add_data(tests):
    """"""
    # Creating a Instance of new artist


    """tests = [{"table_name": test_name,
               "title": "Test001",
               "description": "Test 01 probe function",
                "test_id": 0

               },
              {"table_name": test_name,
               "title": "Test002",
               "description": "Test 02 probe function",
               "test_id": 1
               },
             {"table_name": test_name,
              "title": "Test004",
              "description": "Test 04 probe function",
              "test_id": 2
              },
              {"table_name": test_name,
               "title": "Test005",
               "description": "Test 05 Device",
               "test_id": 3
               }
              ]"""

    for test in tests:
        a = Tests(**test)


if __name__ == "__main__":
    add_data()

    # use db_session as a context manager
    #with pny.db_session:
     #   a = Artist(name="Skillet")