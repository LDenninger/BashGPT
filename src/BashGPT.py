import os
import joblib
from typing import Optional, Union, List, Tuple, Dict, Any

from models.ModelInterface import ModelInterface

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

class BashGPT:
    """
        A simple bash interface for a chat bot.
    """
    def __init__(self, 
                 chat_model:ModelInterface, 
                 chat_name:str='default',
                 keep_in_ram:bool=False):
        self.chat_model = chat_model
        ##-- Parameters --##
        self.chat_name = chat_name
        self.keep_in_ram = keep_in_ram
        ##-- Data structures --##
        self.message_query = []

        self.save()
        os.system('clear')
        return
    
    def __call__(self):
        """
            Request a chat input and give the response from the given chat model.

        """
        if not self.keep_in_ram:
            self.load()
        _ = self.request_input()
        _ = self.request_response()
        self.print()
        if not self.keep_in_ram:
            self.save()
            self.clear()


    def print(self):
        os.system('clear')
        # Print previous messages
        for i, message in enumerate(self.past_messages):
            speaker = message['role']
            content = message['content']
            if speaker == 'user':
                print_white(f"User:\n{content}")
            else:
                print_green(f"Assistant:\n{content}")
            print('\n')

    def print_error(self, message: str):
        print_red(f'\n ERROR: {message}\n')

    def request_response(self, message:str=None):
        if message is not None:
            self.message_query.append({
                'role': 'user',
                'content': message
            })
        
    def request_input(self):
        # Request user input
        user_input = input(">>> ")
        new_message = {
            'role': 'user',
            'content': user_input
        }
        self.past_messages.append(new_message)
        print_red("\n Awaiting response...\n")

        return user_input
    
    
    ##-- Chat Management --##
    def new_chat(self, chat_name: str='default'):
        self.chat_name = chat_name

    def chat_exists(self, chat_name:str=None):
        if chat_name is None:
            chat_name = self.chat_name
        return os.path.exists(os.path.join('resources','chats',chat_name+'.joblib'))

    def load(self, chat_name:str=None):
        if chat_name is None:
            chat_name = self.chat_name
        try:
            self.message_query = joblib.load(os.path.join('resources','chats',chat_name+'.joblib'))
        except FileNotFoundError:
            self.print_error(f'Chat not found: {chat_name}')
    
    def save(self, messages: List[Dict[str,str]]=None):
        if messages is None:
            messages = self.message_query
        try:
            joblib.dump(messages,os.path.join('resources','chats',self.chat_name+'.joblib'))
        except:
            self.print_error(f'Could not save chat: {self.chat_name}')

    def clear(self):
        self.message_query = []


    ##-- Input Processing --##
    def check_command(self, input: str):
        """
            Check if a command was provided in the prompt and execute it.
        """
        pos_to_remove:List[Tuple[int,int]] = []
        pos_to_insert:List[int] = []
        text_to_insert:List[str] = []

        for i, char in enumerate(input):
            # Detect command symbol !
            if char=='!':
                # If a command symbol was detected, process the given command and parameter
                try:
                    complete_end_ind = input[i:].index(' ')
                except ValueError:
                    complete_end_ind = len(input)-1
                try:
                    param_start_ind = input[i:].index('(')
                except ValueError:
                    param_start_ind = len(input)
                try:
                    param_end_ind = input[i:].index(')')
                except ValueError:
                    param_end_ind = len(input)

                if param_start_ind>complete_end_ind:
                    command_end_ind = complete_end_ind
                else:
                    command_end_ind = param_start_ind
                
                command = input[i+1:command_end_ind]

                ##-- Commands --##
                # !clear -> clear the context of the chat bot
                if command.lower() == 'clear':
                    self.chat_model.clear()
                    pos_to_remove.append((i, command_end_ind+1))

                # !load(file) -> Load a file into the context of the chat bot
                # For this we simply insert it in the position where the command was given
                elif command.lower() == 'load':
                    if param_start_ind == len(input) or param_end_ind == len(input):
                        self.print_error('Please provide a file to load')
                        continue
                    file_path=input[param_start_ind+1:param_end_ind]
                    try:
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                    except FileNotFoundError:
                        self.print_error(f'File not found: {file_path}')
                        continue
                    pos_to_remove.append((i, param_end_ind+1))
                    pos_to_insert.append(i)
                    text_to_insert.append(file_content)

        for (start, end) in pos_to_remove:
            input = input[:start] + input[end:]

        for ind, text in zip(pos_to_insert, text_to_insert):
            input = input[:ind] + text + input[ind:]

        return input