from typing import List

import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow


class Database:
    stats_table_name = 'stats'

    def __init__(self, db_uri: str):
        # TODO: use env var DB_URI
        self.uri = db_uri
        self.conn = psycopg2.connect(db_uri)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def insert_stat(
        self,
        url: str,
        res_time_sec: float,
        status_code: int,
        pattern_exists: bool,
        pattern_match: str,
    ):
        insert_stat_sql = f"""INSERT INTO {self.stats_table_name} (
        url,
        response_time_sec,
        status_code,
        pattern_exists,
        pattern_match
        ) VALUES (%s, %s, %s, %s, %s)"""

        result = self.cursor.execute(
            insert_stat_sql,
            (url, res_time_sec, status_code, pattern_exists, pattern_match),
        )
        self.conn.commit()
        return result

    def get_stats(self) -> List[RealDictRow]:
        get_stats_sql = f"""SELECT * FROM {self.stats_table_name};"""
        self.cursor.execute(get_stats_sql)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        self.cursor.close()
