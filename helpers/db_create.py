import pony.orm as pny

unicode = str

database = pny.Database("sqlite",
                        "test.db",
                        create_db=True)


########################################################################
class Table(database.Entity):
    """
    Pony ORM model of the Artist table
    """
    name = pny.Required(unicode)
    tests = pny.Set("Tests")


########################################################################
class Tests(database.Entity):
    """
    Pony ORM model of album table
    """
    table_name = pny.Required(Table)
    title = pny.Required(unicode)
    description = pny.Required(unicode)
    test_id = pny.Required(int)


# turn on debug mode
#pny.sql_debug(True)

# map the models to the database
# and create the tables, if they don't exist
database.generate_mapping(create_tables=True)