import plotly
import plotly.graph_objects as go
import pandas
from plotly.subplots import make_subplots
from goal_tracker.src.io.query_runner import QueryRunner


class ContextManager(object):

    def __init__(self, configs):
        self.config = configs
        self.query_runner = QueryRunner(configs)
        self.query_runner.create_all_tables()


    def get_all_goals(self):
        return self.query_runner.get_all_goals()

    def get_goals_for_date(self, chosen_date):
        return self.query_runner.get_all_goals(date=chosen_date)

    def record_new_goal(self, goal_type, goal_date, goal_description):
        self.query_runner.record_new_goal(goal_type, goal_date, goal_description)

    def record_goal_progress(self, goal_id, progress):
        self.query_runner.record_goal_progress(goal_id, progress)

    def get_progress_for_goal(self, goal_id):
        return self.query_runner.get_progress_for_goal(goal_id)

    def complete_goal(self, goal_id):
        self.query_runner.complete_goal(goal_id)
