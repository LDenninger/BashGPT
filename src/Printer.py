import os

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

class SimpleBash:
    """
        A simple bash interface for a chat bot.
    """
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
                print_white(f"User:\n{content}")
            else:
                print_green(f"Assistant:\n{content}")
            print('\n')
    def request_input(self):
        # Request user input
        user_input = input(">>> ")
        print_red("\n Awaiting response...\n")
        return user_input