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

class RecordMenu(InteractiveMenu):

    def title(self):
        return "Record"

    def main_loop(self):
        form_results = self.interactive_form(
            [
                {
                    "question": "What goal did you work towards?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "goal",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "What specifically did you do? Hit enter to skip",
                    "expected_response_type": "VARCHAR",
                    "return_as": "progress_type",
                    "default": "",
                    "allow_empty": True
                },
                {
                    "question": "How many minutes did you work towards the goal?",
                    "expected_response_type": "INT",
                    "return_as": "minutes",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "What date? (YYYY-MM-DD) Hit enter for today",
                    "expected_response_type": "YYYYMMDD_Date",
                    "return_as": "date",
                    "default": datetime.now().strftime("%Y-%m-%d"),
                    "allow_empty": False
                }
            ]
        )
        if form_results["user_accept"] != True:
            print("Aborting!")
            return
        form_results.pop("user_accept")
        for answer_key in form_results.keys():
            if not form_results[answer_key]["valid"]:
                print("%s is not a valid value! Aborting" % answer_key)
                return

        goal = form_results["goal"]["value"]
        progress_type = form_results["progress_type"]["value"]
        minutes = form_results["minutes"]["value"]
        date = form_results["date"]["value"]

        self.manager.record_goal_progress(goal, minutes, date, progress_type)

class ReadMenu(InteractiveMenu):

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




