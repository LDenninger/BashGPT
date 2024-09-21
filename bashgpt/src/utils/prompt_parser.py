from abc import abstractmethod
import re
from typing import * 

class Command:
    
    def __init__(self, command: str, help:str = ""):
        self.command:str = command
        self._help = help

        return
    
    def __call__(self, input:str) -> str:
        starts = []; ends = []
        for match in re.finditer(re.escape(self.command), input):
            # Append the start position of each match
            start = match.start()
            end = match.end()
            starts.append(start)
            ends.append(end)

        return self._execute(input, starts, ends)
    
    @abstractmethod
    def _execute(self, string:str, starts:List[int], end:List[int]) -> str:
        raise NotImplementedError("Subclasses must implement _execute method")
    
    def to_dict(self) -> Dict[str, Union[str, List[int]]]:
        return {
            'command': self.command,
            'help': self._help,
        }  # return a dict representation of the command object with the command, help, and matching positions in the input string.
    
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


