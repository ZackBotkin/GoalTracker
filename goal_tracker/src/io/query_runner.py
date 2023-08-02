import sqlite3

class QueryRunner(object):

    def __init__(self, config):
        self.config = config
        self.database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("database_name")
        )

    def run_sql(self, sql_str):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute(sql_str)
        conn.commit()

    def fetch_sql(self, sql_str):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute(sql_str)
        results = query.fetchall()
        return results

    def create_all_tables(self):
        self.create_table()

    def create_table(self):
        sql_str = "CREATE TABLE goal_progress(date DATE, goal VARCHAR, minutes INT, progress_type VARCHAR)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError:
            pass

    def insert_goal_progress(self, goal, minutes, date, progress_type=None):
        sql_str = ""
        if progress_type is None:
            sql_str = "INSERT INTO goal_progress ('goal', 'minutes', 'date') VALUES ('%s', '%s', '%s')" % (goal, minutes, date)
        else:
            sql_str = "INSERT INTO goal_progress ('goal', 'minutes', 'date', 'progress_type') VALUES ('%s', '%s', '%s', '%s')" % (goal, minutes, date, progress_type)
        self.run_sql(sql_str)

    def get_goal_progress(self):
        sql_str = "SELECT * FROM goal_progress"
        return self.fetch_sql(sql_str)

