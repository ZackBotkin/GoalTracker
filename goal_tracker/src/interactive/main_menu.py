from datetime import datetime, timedelta
from interactive_menu.src.interactive_menu import InteractiveMenu


class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMenu(manager, self.path),
            ReadMenu(manager, self.path),
            #GraphMenu(manager, self.path)
        ]

    def title(self):
        return "Goal Tracker"

#
#   Record
#
class RecordMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordNewMenu(manager, self.path),
            RecordProgressMenu(manager, self.path),
            RecordFinishMenu(manager, self.path)
        ]

    def title(self):
        return "Record"

class RecordNewMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordNewAuxiliaryGoalMenu(manager, self.path)
        ]

    def title(self):
        return "New"

class RecordNewAuxiliaryGoalMenu(InteractiveMenu):

    def title(self):
        return "Auxiliary"

    def main_loop(self):
        form_results = self.interactive_form_and_validate(
            [
                {
                    "question": "What date? (ENTER for today)",
                    "expected_response_type": "YYYYMMDD_Date",
                    "return_as": "goal_date",
                    "default": datetime.now().strftime("%Y-%m-%d"),
                    "allow_empty": False
                },
                {
                    "question": "Description of the goal?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "goal_description",
                    "default": "",
                    "allow_empty": False
                }
            ]
        )
        if form_results is not None:
            goal_date = form_results["goal_date"]["value"]
            goal_description = form_results["goal_description"]["value"]
            self.manager.record_new_auxiliary_goal(goal_date, goal_description)


class RecordProgressMenu(InteractiveMenu):

    def title(self):
        return "Progress"

    def main_loop(self):

        now = datetime.now()
        now_str = datetime.now().strftime('%Y-%m-%d')
        all_goals = self.manager.get_auxiliary_goals_for_date(now_str)
        menu = {}
        number = 1
        for goal in all_goals:
            menu[number] = goal
            number = number + 1

        for goal in menu.items():
            number = goal[0]
            auxiliary_goal_description = goal[1][2]
            auxiliary_goal_completed = goal[1][3]
            auxiliary_goal_completed_text = "Not Completed"
            if auxiliary_goal_completed == 1:
                auxiliary_goal_completed_text = "Completed"
            print (str(number) + ": " + auxiliary_goal_description + " (" + auxiliary_goal_completed_text + ")\n")

        form_results = self.interactive_form_and_validate([
            {
                "question": "Which goal to update (select the number)",
                "expected_response_type": "INT",
                "return_as": "goal_selection_number",
                "default": "",
                "allow_empty": False
            },
        ])
        if form_results is not None:
            chosen_goal_number = form_results["goal_selection_number"]["value"]
            chosen_goal_number = int(chosen_goal_number)
            chosen_goal = menu[chosen_goal_number]
            chosen_goal_id = chosen_goal[0]

            form_results = self.interactive_form_and_validate([
                {
                    "question": "What progress has been made?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "goal_progress",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "What percentage is the goal now at? (enter to skip)",
                    "expected_response_type": "FLOAT",
                    "return_as": "goal_percentage_completion",
                    "default": None,
                    "allow_empty": True ## TODO : there is a bug here because of the expected response type, we can't allow None
                }
            ])
            if form_results is not None:
                progress = form_results["goal_progress"]["value"]
                percentage = form_results["goal_percentage_completion"]["value"]
                self.manager.record_auxiliary_goal_progress(chosen_goal_id, progress, percentage)

                if percentage is not None and float(percentage) >= 100:
                    self.manager.complete_auxiliary_goal(chosen_goal_id)


class RecordFinishMenu(InteractiveMenu):

    def title(self):
        return "Finish"

    def main_loop(self):

        now = datetime.now()
        now_str = datetime.now().strftime('%Y-%m-%d')
        all_goals = self.manager.get_auxiliary_goals_for_date(now_str)
        menu = {}
        number = 1
        for goal in all_goals:
            menu[number] = goal
            number = number + 1

        for goal in menu.items():
            number = goal[0]
            value = goal[1][2]
            print (str(number) + ": " + value)

        form_results = self.interactive_form_and_validate([
            {
                "question": "Which goal to update (select the number)",
                "expected_response_type": "INT",
                "return_as": "goal_selection_number",
                "default": "",
                "allow_empty": False
            }
        ])
        if form_results is not None:
            chosen_goal_number = form_results["goal_selection_number"]["value"]
            chosen_goal_number = int(chosen_goal_number)
            chosen_goal = menu[chosen_goal_number]
            chosen_goal_id = chosen_goal[0]
            self.manager.complete_auxiliary_goal(chosen_goal_id)

#
#   Read
#

class ReadMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ReadTodayMenu(manager, self.path),
            ReadTomorrowMenu(manager, self.path),
            ReadYesterdayMenu(manager, self.path)
        ]

    def title(self):
        return "Read"

class ReadTodayMenu(InteractiveMenu):

    def title(self):
        return "Today"

    def main_loop(self):
        now = datetime.now()
        now_str = datetime.now().strftime('%Y-%m-%d')
        all_goals = self.manager.get_auxiliary_goals_for_date(now_str)
        for goal in all_goals:
            goal_id = goal[0]
            goal_date = goal[1]
            goal_description = goal[2]
            goal_completed = goal[3]
            all_progress = self.manager.get_progress_for_auxiliary_goal(goal_id)
            goal_completed_text = "Not Completed"
            if goal_completed == True:
                goal_completed_text = "Completed!"
            print("> %s (%s)" % (goal_description, goal_completed_text))
            if len(all_progress) == 0:
                print ("\tNo progress")
            else:
                for progress in all_progress:
                    progress_id = progress[0]
                    goal_id = progress[1]
                    progress_description = progress[2]
                    print ("\t >> %s" % progress_description)
            print("\n")

class ReadTomorrowMenu(InteractiveMenu):

    def title(self):
        return "Tomorrow"

    def main_loop(self):
        now = datetime.now()
        now_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        all_goals = self.manager.get_auxiliary_goals_for_date(now_str)
        for goal in all_goals:
            goal_id = goal[0]
            goal_date = goal[1]
            goal_description = goal[2]
            goal_completed = goal[3]
            all_progress = self.manager.get_progress_for_auxiliary_goal(goal_id)
            goal_completed_text = "Not Completed"
            if goal_completed == True:
                goal_completed_text = "Completed!"
            print("> %s (%s)" % (goal_description, goal_completed_text))
            if len(all_progress) == 0:
                print ("\tNo progress")
            else:
                for progress in all_progress:
                    progress_id = progress[0]
                    goal_id = progress[1]
                    progress_description = progress[2]
                    print ("\t >> %s" % progress_description)
            print("\n")

class ReadYesterdayMenu(InteractiveMenu):

    def title(self):
        return "Yesterday"

    def main_loop(self):
        now = datetime.now()
        now_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        all_goals = self.manager.get_auxiliary_goals_for_date(now_str)
        for goal in all_goals:
            goal_id = goal[0]
            goal_date = goal[1]
            goal_description = goal[2]
            goal_completed = goal[3]
            all_progress = self.manager.get_progress_for_auxiliary_goal(goal_id)
            goal_completed_text = "Not Completed"
            if goal_completed == True:
                goal_completed_text = "Completed!"
            print("> %s (%s)" % (goal_description, goal_completed_text))
            if len(all_progress) == 0:
                print ("\tNo progress")
            else:
                for progress in all_progress:
                    progress_id = progress[0]
                    goal_id = progress[1]
                    progress_description = progress[2]
                    print ("\t >> %s" % progress_description)
            print("\n")



