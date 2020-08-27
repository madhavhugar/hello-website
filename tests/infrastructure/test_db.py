import psycopg2

from src.infrastructure.db import Database


def test_db_instantiation(mocker):
    mocker.patch('psycopg2.connect')
    mocker.patch('psycopg2.connect.cursor')
    db = Database('db_uri')

    psycopg2.connect.assert_called_once_with('db_uri')
    assert db.stats_table_name == 'stats'


def test_db_close(mocker):
    mocker.patch('psycopg2.connect')
    mocker.patch('psycopg2.connect.cursor')
    db = Database('db_uri')
    db.close()

    db.conn.close.assert_called_once()
    db.cursor.close.assert_called_once()


def test_insert_stat(mocker):
    mocker.patch('psycopg2.connect')
    mocker.patch('psycopg2.connect.cursor')
    db = Database('db_uri')
    db.insert_stat('url', 12.2, 200, False, 'pattern')
    insert_stat_sql = f"""INSERT INTO {db.stats_table_name} (
        url,
        response_time_sec,
        status_code,
        pattern_exists,
        pattern_match
        ) VALUES (%s, %s, %s, %s, %s)"""

    db.cursor \
      .execute \
      .assert_called_once_with(
          insert_stat_sql,
          ('url', 12.2, 200, False, 'pattern'),
        )
