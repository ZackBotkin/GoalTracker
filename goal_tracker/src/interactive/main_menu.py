from datetime import datetime
from interactive_menu.src.interactive_menu import InteractiveMenu


class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMenu(manager, self.path),
            ReadMenu(manager, self.path),
            GraphMenu(manager, self.path)
        ]

    def title(self):
        return "Main"

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

    def title(self):
        return "New"

    def main_loop(self):
        form_results = self.interactive_form_and_validate(
            [
                {
                    "question": "Daily or Weekly goal?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "goal_type",
                    "default": "",
                    "allow_empty": False
                },
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
            goal_type = form_results["goal_type"]["value"]
            goal_date = form_results["goal_date"]["value"]
            goal_description = form_results["goal_description"]["value"]
            self.manager.record_new_goal(goal_type, goal_date, goal_description)


class RecordProgressMenu(InteractiveMenu):

    def title(self):
        return "Progress"

    def main_loop(self):
        form_results = form_results.self.interactive_form_and_validate(
            [
                {
                    "question": "For which date? (ENTER for today)",
                    "expected_response_type": "YYYYMMDD_Date",
                    "return_as": "chosen_date",
                    "default": "",
                    "allow_empty": True
                }
            ]
        )
        if form_results:
            chosen_date = form_results["chosen_date"]["value"]
            goals_for_date = self.manager.get_goals_for_date(chosen_date)
            if len(goals_for_date) is None:
                print("No goals for date")
            else:
                print("Add progress for which goal")
                ## TODO

class RecordFinishMenu(InteractiveMenu):

    def title(self):
        return "Finish"

#
#   Read
#

class ReadMenu(InteractiveMenu):

    def title(self):
        return "Read"

    def main_loop(self):
        all_goals = self.manager.get_all_goals()
        for goal in all_goals:
            print(goal)




#
#   Old stuff
#

class OldReadMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            TotalsMenu(manager, self.path)
        ]

    def title(self):
        return "Read"

class TotalsMenu(InteractiveMenu):

    def title(self):
        return "Totals"

    def main_loop(self):
        all_goals = {}
        all_goal_progress_rows = self.manager.read_goal_progress()
        for progress in all_goal_progress_rows:
            date = progress[0]
            goal = progress[1]
            minutes = progress[2]
            progress_type = progress[3]
            if goal not in all_goals:
                all_goals[goal] = 0
            all_goals[goal] += minutes
        print("|")
        print("|")
        for goal, minutes in all_goals.items():
            hours = minutes/60
            quarter = (hours/2500)*100
            half = (hours/5000)*100
            three_quarters = (hours/7500)*100
            mastery = (hours/10000)*100
            print("|\t> %s: %f hours" % (goal, hours))
            print("|")
            print("|\t\t> %f percent of the way to 2500 hours" % quarter)
            print("|\t\t> %f percent of the way to 5000 hours" % half)
            print("|\t\t> %f percent of the way to 7500 hours" % three_quarters)
            print("|\t\t> %f percent of the way to mastery" % mastery)
            print("|")
        print("|")
        print("|")

class GraphMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            BarGraphMenu(manager, self.path)
        ]

    def title(self):
        return "Graphs"


class BarGraphMenu(InteractiveMenu):

    def title(self):
        return "Bar"

    def main_loop(self):
        self.manager.bar_graph_all_goals()




