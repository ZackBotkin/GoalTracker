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

    def get_all_auxiliary_goals(self):
        return self.query_runner.get_all_auxiliary_goals()

    def get_auxiliary_goals_for_date(self, chosen_date):
        return self.query_runner.get_all_auxiliary_goals(date=chosen_date)

    def record_new_auxiliary_goal(self, date, description):
        self.query_runner.record_new_auxiliary_goal(date, description)

    def record_auxiliary_goal_progress(self, goal_id, description, percentage):
        self.query_runner.record_auxiliary_goal_progress(goal_id, description, percentage)

    ## TODO : maybe.. this assumes we can never make backwards progress
    def get_percentage_done_for_goal(self, goal_id):
        all_progress = self.get_progress_for_auxiliary_goal(goal_id)
        highest_percentage = 0
        for progress in all_progress:
            progress_id = progress[0]
            goal_id = progress[1]
            description = progress[2]
            this_percentage = float(progress[3])
            if this_percentage > highest_percentage:
                highest_percentage = this_percentage
        return highest_percentage

    def get_progress_for_auxiliary_goal(self, goal_id):
        return self.query_runner.get_progress_for_auxiliary_goal(goal_id)

    def complete_auxiliary_goal(self, goal_id):
        self.query_runner.complete_auxiliary_goal(goal_id)
