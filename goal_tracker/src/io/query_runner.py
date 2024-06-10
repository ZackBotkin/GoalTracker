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
        except sqlite3.OperationalError:
            pass

    def create_progress_table(self):
        sql_str = "CREATE TABLE progress(progress_id INTEGER PRIMARY KEY AUTOINCREMENT, "
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError:
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
        sql_str = "INSERT INTO progress ('goal_id', 'description') VALUES ('%s', '%s')" % (goal_id, goal_progress)
        self.run_sql(sql_st)


    ##### OLD STUFF BELOW HERE


    def old_create_table(self):
        sql_str = "CREATE TABLE goal_progress(date DATE, goal VARCHAR, minutes INT, progress_type VARCHAR)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError:
            pass

    def old_insert_goal_progress(self, goal, minutes, date, progress_type=None):
        sql_str = ""
        if progress_type is None:
            sql_str = "INSERT INTO goal_progress ('goal', 'minutes', 'date') VALUES ('%s', '%s', '%s')" % (goal, minutes, date)
        else:
            sql_str = "INSERT INTO goal_progress ('goal', 'minutes', 'date', 'progress_type') VALUES ('%s', '%s', '%s', '%s')" % (goal, minutes, date, progress_type)
        self.run_sql(sql_str)

    def old_get_goal_progress(self, goal_name=None):
        sql_str = "SELECT * FROM goal_progress"
        if goal_name is not None:
                sql_str += " WHERE goal = '%s'" % goal_name
        return self.fetch_sql(sql_str)

