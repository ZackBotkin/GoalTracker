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
