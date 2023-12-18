import argparse
import os
import curses
import sys
import json
from src.ChatGPT import ChatGPT

##-- Color Schemes --##
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

print_red = lambda s: print(f"{RED}{s}{RESET}")
print_blue = lambda s: print(f"{BLUE}{s}{RESET}")
print_green = lambda s: print(f"{GREEN}{s}{RESET}")
print_white = lambda s: print(f"{WHITE}{s}{RESET}")


class InteractiveBash:
    def __init__(self):

        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # User's messages
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Bot's messages

        return
    
    def print(self, messages: list):
        # Print previous messages
        import ipdb; ipdb.set_trace()
        for i, message in enumerate(messages):
            speaker = next(iter(messages.keys()))
            content = next(iter(messages.values()))
            color = curses.color_pair(1) if speaker == 'user' else curses.color_pair(2)
            self.screen.addstr(i, 0, f"{speaker}: {content}", color)
        # Request user input
        self.screen.addstr(len(messages), 0, "")

class SimpleBash:
    def __init__(self):
        os.system('clear')
        return
    
    def print(self, messages: list):
        os.system('clear')
        # Print previous messages
        for i, message in enumerate(messages):
            speaker = message['role']
            content = message['content']
            if speaker == 'user':
                print_green(f"User:\n{content}")
            else:
                print_white(f"Assistant:\n{content}")

    def request_input(self):
        user_input = input(">>> ")
        print_red("\n Awaiting response...\n")
        return user_input
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default="gpt-3.5-turbo")
    parser.add_argument('--mode', type=str, default='assistant')
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--max_tokens', type=int, default=100)
    parser.add_argument('--use_past', type=bool, default=True)
    parser.add_argument('--cmd_line', type=bool, default=True)
    args = parser.parse_args()

    with open('resources/config.json', 'r') as f:
        config = json.load(f)

    chat_gpt = ChatGPT(args.model_name, args.mode, args.temperature, args.max_tokens, config['OPENAI_API_KEY'])
    

    printer = SimpleBash()

    while True:
        try:
            user_input = printer.request_input()
            if user_input == 'exit':
                break
            else:
                response = chat_gpt(user_input, cmd_line=True, use_past=False)
                printer.print(chat_gpt.get_messages())
        except KeyboardInterrupt:
            break
    
