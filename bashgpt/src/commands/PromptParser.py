from abc import abstractmethod
import re
from typing import * 
import copy

class Command:
    
    def __init__(self, command: str, command_prefix: str="\\", help:str = ""):
        self.command:str = command_prefix+command
        self._help = help

        return
    
    def __call__(self, input:str) -> str:
        start = 0

        while True:
            match = input[start:].find(self.command)
            # If no match is found, break the loop
            if not match or match == -1:
                break

            # Get the actual match position in the original string
            match_start = start + match
            match_end = start + match + len(self.command)

            input, start = self._execute(input, match_start, match_end)

        return input
    
    
    @abstractmethod
    def _execute(self, string:str, start:int, end:int) -> Tuple[str, int]:
        raise NotImplementedError("Subclasses must implement _execute method")
    
    def to_dict(self) -> Dict[str, Union[str, List[int]]]:
        return {
            'command': self.command,
            'help': self._help,
        }  # return a dict representation of the command object with the command, help, and matching positions in the input string.
    
    def _remove_substring(self, string: str, start:int, end:int) -> str:
        return string[:start] + string[end:]
    
    def _insert_substring(self, string: str, sub_string: str, position: int) -> str:
        return string[:position] + sub_string + string[position:]
    
    def _get_arguments(self, string: str, start: int, end: int) -> Tuple[List[str], int]:

        arg_start = end
        arg_end = end
        if string[arg_start] != "{":
            return []
        arg_end = string.find("}", arg_start)
        arg_string = string[(arg_start+1):arg_end]

        args = arg_string.split(",")
        args = [arg.strip() for arg in args]

        return args, arg_end+1


    def __str__(self) -> str:
        return f"Command(command='{self.command}', help='{self._help}')"
    

class PromptParser:

    def __init__(self, commands: List[Command]=None):

        self.commands = commands if commands else []
        return
    
    def add_command(self, command: Command):
        self.commands.append(command)
        return self
    
    def __call__(self, input: str) -> str:
        output = input
        for command in self.commands:
            output = command(output)
        return output
    
    def __str__(self) -> str:
        return f"PromptParser(commands={self.commands})"


