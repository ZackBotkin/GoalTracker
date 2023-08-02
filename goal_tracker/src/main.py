import argparse

from goal_tracker.src.config.config import Configs
from goal_tracker.src.context_manager import ContextManager
from goal_tracker.src.interactive.main_menu import MainMenu

def main():

    parser = argparse.ArgumentParser(description= 'default parser')
    parser.add_argument('--config_file', help='the configuration file')
    args = parser.parse_args()

    configs = Configs(args.config_file)
    context_manager = ContextManager(configs)
    main_menu = MainMenu(context_manager)
    main_menu.main_loop()

if __name__ == '__main__':
    main()
