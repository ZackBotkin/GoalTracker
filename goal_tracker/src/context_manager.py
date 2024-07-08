import plotly
import plotly.graph_objects as go
import pandas
import matplotlib.pyplot as plt
import numpy as np
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from goal_tracker.src.io.query_runner import QueryRunner

def get_gradient_color(value, min_value=0, max_value=100):

    ratio = (value - min_value) / (max_value - min_value)
    red = int((1-ratio) * 255)
    green = int(ratio * 255)
    return (red/255.0, green/255.0, 0)

def plot_pie_chart(values, labels, sizes):
    colors = [get_gradient_color(value) for value in values]
    plt.pie(sizes, labels=labels, colors=colors, startangle=140, radius=0.3, wedgeprops={"edgecolor":"black", "linewidth": 1.5})
    plt.axis('equal')
    plt.show()

def plot_multiple_pie_charts(pie_data):

    num_pies = len(pie_data)
    cols = 2
    rows = (num_pies + 1) // cols

    fig, axs = plt.subplots(rows, cols, figsize=(10, 5* rows))

    fig.subplots_adjust(hspace=0.5, wspace=0.5)

    for i, data in enumerate(pie_data):

        row = i // cols
        col = i % cols
        ax = axs[row, col] if rows > 1 else axs[col]

        values = data['values']
        labels = data['labels']
        sizes = data['sizes']
        colors = [get_gradient_color(value) for value in values]

        ax.pie(sizes, labels=labels, colors=colors, startangle=140, radius=0.3, wedgeprops={"edgecolor":"black", "linewidth": 1.5})
        ax.axis('equal')
        ax.set_title(data['title'])

    # remove empty subplots
    for j in range(i+1, rows * cols):
        fig.delaxes(axs.flatten()[j])

    plt.tight_layout()
    plt.show()

def is_within_last_n_weeks(n, date):

    today = datetime.today()
    two_weeks_ago = today - timedelta(weeks=n)
    return two_weeks_ago <= date <= today

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
            this_percentage = 0
            try:
                this_percentage = float(progress[3])
            except:
                pass
            if this_percentage > highest_percentage:
                highest_percentage = this_percentage
        return highest_percentage

    def get_progress_for_auxiliary_goal(self, goal_id):
        return self.query_runner.get_progress_for_auxiliary_goal(goal_id)

    def complete_auxiliary_goal(self, goal_id):
        self.query_runner.complete_auxiliary_goal(goal_id)

    def pie_chart_for_date(self, chosen_date):
        all_goals_for_date = self.query_runner.get_all_auxiliary_goals(date=chosen_date)
        values = []
        labels = []
        sizes = []
        for auxiliary_goal in all_goals_for_date:
            auxiliary_goal_id = auxiliary_goal[0]
            auxiliary_goal_description = auxiliary_goal[2]
            percentage_done = self.get_percentage_done_for_goal(auxiliary_goal_id)
            values.append(percentage_done)
            labels.append("%s : %.2f percent done" % (auxiliary_goal_description, percentage_done))
            sizes.append(10)

        plot_pie_chart(values, labels, sizes)

    def plot_all_pie_charts(self):
        all_goals = self.query_runner.get_all_auxiliary_goals()
        goal_hash = {}
        for auxiliary_goal in all_goals:
            auxiliary_goal_id = auxiliary_goal[0]
            auxiliary_goal_date = auxiliary_goal[1]
            auxiliary_goal_description = auxiliary_goal[2]

            date_obj = datetime.strptime(auxiliary_goal_date, "%Y-%m-%d")
            if not is_within_last_n_weeks(1, date_obj):
                pass
            else:
                if auxiliary_goal_date not in goal_hash:
                    goal_hash[auxiliary_goal_date] = {
                        "values": [],
                        "labels": [],
                        "sizes": []
                    }
                percentage_done = self.get_percentage_done_for_goal(auxiliary_goal_id)
                goal_hash[auxiliary_goal_date]["values"].append(percentage_done)
                goal_hash[auxiliary_goal_date]["labels"].append("%s : %.2f percent done" % (auxiliary_goal_description, percentage_done))
                goal_hash[auxiliary_goal_date]["sizes"].append(10)

        pie_data = []
        for date in goal_hash.keys():
            data = goal_hash[date]
            pie_data.append({
                "title" : date,
                "values": data["values"],
                "labels": data["labels"],
                "sizes": data["sizes"]
            })

        plot_multiple_pie_charts(pie_data)

