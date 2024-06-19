import argparse
from goal_tracker.src.context_manager import ContextManager
from goal_tracker.src.interactive.main_menu import MainMenu
from config_reader.src.config_reader import Configs

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
