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


    def record_goal_progress(self, goal, minutes, date, progress_type=None):
        self.query_runner.insert_goal_progress(goal, minutes, date, progress_type)

    def read_goal_progress(self):
        goal_progress = self.query_runner.get_goal_progress()
        return goal_progress


    def bar_graph_all_goals(self):

        all_goal_progress = self.query_runner.get_goal_progress()

        goals = {}

        for goal_progress in all_goal_progress:
            date = goal_progress[0]
            goal_name = goal_progress[1]
            minutes = goal_progress[2]
            specific_activity = goal_progress[3]

            if goal_name not in goals:
                goals[goal_name] = {}

            if date not in goals[goal_name]:
                goals[goal_name][date] = []

            goals[goal_name][date].append({"specific_activity": specific_activity, "minutes": minutes})

        for goal_name, dates in goals.items():
            x_vals = []
            y_vals = []

            for date, activities in dates.items():
                x_vals.append(date)
                total_minutes = 0
                for activity in activities:
                    total_minutes += activity["minutes"]
                y_vals.append(total_minutes)

            import plotly.express as px
            df = pandas.DataFrame({
                'x': x_vals,
                'y': y_vals
            })
            fig = px.bar(df, x='x', y='y', title=goal_name)
            fig.write_html('%s.html' % goal_name, auto_open=True)

        return
