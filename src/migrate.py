import os

from infrastructure.db import Database


def create_stats_table(db: Database) -> None:
    create_table_sql = f"""CREATE TABLE {db.stats_table_name} (
    id SERIAL PRIMARY KEY,
    url varchar(300),
    response_time_sec float,
    status_code integer,
    pattern_exists boolean,
    pattern_match varchar(300),
    created_at timestamp default current_timestamp
    );"""
    db.cursor.execute(create_table_sql)
    db.conn.commit()


def create_schema(db: Database) -> None:
    SCHEMA_NAME = 'website_stats'
    create_schema_sql = f'CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}'
    db.cursor.execute(create_schema_sql)
    db.conn.commit()


# def drop_table(db: Database) -> None:
#     drop_table_sql = f"""DROP TABLE {db.stats_table_name};"""
#     db.cursor.execute(drop_table_sql)
#     db.conn.commit()


if __name__ == "__main__":
    print('Creating schema and tables on the database...')
    DB_URI = os.getenv('DB_URI')
    db = Database(DB_URI)
    # drop_table(db)
    create_schema(db)
    create_stats_table(db)
    db.close()
