import sqlite3
from query_runner.src.runner import SqlLiteQueryRunner


class QueryRunner(SqlLiteQueryRunner):

    def create_all_tables(self):
        #self.create_goals_table()
        self.create_primary_goals_table()
        self.create_auxiliary_goals_table()
        self.create_progress_table()

    def create_primary_goals_table(self):
        sql_str = "CREATE TABLE primary_goals(primary_goal_id INTEGER PRIMARY KEY AUTOINCREMENT, date_introduced DATE, primary_goal_description VARCHAR)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError as e:
            pass

    def create_auxiliary_goals_table(self):
        sql_str = "CREATE TABLE auxiliary_goals(auxiliary_goal_id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, auxiliary_goal_description VARCHAR, auxiliary_goal_completed BOOLEAN)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError as e:
            pass

    def create_progress_table(self):
        sql_str = "CREATE TABLE progress(progress_id INTEGER PRIMARY KEY AUTOINCREMENT, auxiliary_goal_id INTEGER, progress_description VARCHAR, progress_percentage FLOAT, FOREIGN KEY (auxiliary_goal_id) REFERENCES auxiliary_goals(auxiliary_goal_id) ON DELETE CASCADE ON UPDATE CASCADE)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError as e:
            pass

    def get_all_auxiliary_goals(self, date=None):
        sql_str = "SELECT auxiliary_goal_id, date, auxiliary_goal_description, auxiliary_goal_completed FROM auxiliary_goals"
        if date is not None:
            sql_str += " WHERE date='%s'" % date
        return self.fetch_sql(sql_str)

    def record_new_auxiliary_goal(self, date, description):
        sql_str = "INSERT INTO auxiliary_goals ('date', 'auxiliary_goal_description', 'auxiliary_goal_completed') VALUES ('%s', '%s', 'false')" % (date, description)
        self.run_sql(sql_str)

    def record_auxiliary_goal_progress(self, auxiliary_goal_id, description, percentage=None):
        if percentage is not None:
            sql_str = "INSERT INTO progress ('auxiliary_goal_id', 'progress_description', 'progress_percentage') VALUES ('%s', '%s', '%s')" % (auxiliary_goal_id, description, percentage)
            self.run_sql(sql_str)
        else:
            sql_str = "INSERT INTO progress ('auxiliary_goal_id', 'progress_description') VALUES ('%s', '%s')" % (auxiliary_goal_id, description)
            self.run_sql(sql_str)

    def get_progress_for_auxiliary_goal(self, auxiliary_goal_id):
        sql_str = "SELECT progress_id, auxiliary_goal_id, progress_description, progress_percentage FROM progress WHERE auxiliary_goal_id=%s" % int(auxiliary_goal_id)
        return self.fetch_sql(sql_str)

    def complete_auxiliary_goal(self, auxiliary_goal_id):
        sql_str = "UPDATE auxiliary_goals SET auxiliary_goal_completed=true WHERE auxiliary_goal_id='%s'" % auxiliary_goal_id
        self.run_sql(sql_str)
