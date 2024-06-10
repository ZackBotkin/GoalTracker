import sqlite3
from query_runner.src.runner import SqlLiteQueryRunner

class QueryRunner(SqlLiteQueryRunner):

    def create_all_tables(self):
        self.create_goals_table()
        self.create_progress_table()

    def create_goals_table(self):
        sql_str = "CREATE TABLE goals(goal_id INTEGER PRIMARY KEY AUTOINCREMENT, goal_type VARCHAR, goal_date DATE, goal_description VARCHAR, goal_completed BOOLEAN)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError as e:
            pass

    def create_progress_table(self):
        sql_str = "CREATE TABLE progress(progress_id INTEGER PRIMARY KEY AUTOINCREMENT, goal_id INTEGER, progress_description VARCHAR, FOREIGN KEY (goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE ON UPDATE CASCADE)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError as e:
            pass

    def get_all_goals(self, date=None):
        sql_str = "SELECT * FROM goals"
        if date is not None:
            sql_str += " WHERE goal_date='%s'" % date
        return self.fetch_sql(sql_str)

    def record_new_goal(self, goal_type, goal_date, goal_description):
        sql_str = "INSERT INTO goals ('goal_type', 'goal_date', 'goal_description', 'goal_completed') VALUES ('%s', '%s', '%s', 'false')" % (goal_type, goal_date, goal_description)
        self.run_sql(sql_str)

    def record_goal_progress(self, goal_id, goal_progress):
        sql_str = "INSERT INTO progress ('goal_id', 'progress_description') VALUES ('%s', '%s')" % (goal_id, goal_progress)
        self.run_sql(sql_str)


    def get_progress_for_goal(self, goal_id):
        sql_str = "SELECT * FROM progress WHERE goal_id=%s" % int(goal_id)
        return self.fetch_sql(sql_str)

    def complete_goal(self, goal_id):
        sql_str = "UPDATE goals SET goal_completed=true WHERE goal_id='%s'" % goal_id
        self.run_sql(sql_str)
