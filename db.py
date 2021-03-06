from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData

from environs import Env

env = Env()

env.read_env(recurse=True)


connect_string = env.str("DB_CONNECT")

db = create_engine(connect_string)

meta = MetaData(db)
film_table = Table("films", meta, Column("title", String), Column("director", String), Column("year", String))

with db.connect() as conn:

    # Create
    film_table.create()
    insert_statement = film_table.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")
    conn.execute(insert_statement)

    # Read
    select_statement = film_table.select()
    result_set = conn.execute(select_statement)
    for r in result_set:
        print(r)

    # Update
    update_statement = film_table.update().where(film_table.c.year == "2016").values(title="Some2016Film")
    conn.execute(update_statement)

    # Delete
    delete_statement = film_table.delete().where(film_table.c.year == "2016")
    conn.execute(delete_statement)
