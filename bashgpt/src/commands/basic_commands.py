import os
import subprocess
from pathlib import Path

from .PromptParser import Command
from typing import *


class ImportFileCommand(Command):

    def __init__(self, command_prefix: str='\\'):
        super().__init__(
            command="file",
            command_prefix = command_prefix,
            help="Import a file at position."
        )

    def _execute(self, string: str, start:int, end:int) -> str:

        cmd_args, arg_end = self._get_arguments(string, start, end)
        if len(cmd_args) == 0:
            print("Error: No file specified.")
            return string
        elif len(cmd_args) > 1:
            print("Error: Too many arguments.")
            return string
        
        file_path = cmd_args[0]

        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return string
        file_content = self._load(file_path)
        
        output = self._remove_substring(string, start, arg_end)
        output = self._insert_substring(output, file_content, start)

        end_index = start + len(file_content)

        return output, end_index
    
    def _load(self, path: str) -> str:
        with open(path, 'r') as file:
            file_content = file.read()
        return file_content
    
class ExecuteCommand(Command):

    def __init__(self, command_prefix: str='\\'):
        super().__init__(
            command="execute",
            command_prefix = command_prefix,
            help="Execute a file at position."
        )


    def _execute(self, string: str, start: int, end: int) -> str:

        cmd_args, arg_end = self._get_arguments(string, start, end)
        if len(cmd_args) == 0:
            print("Error: No file specified.")
            return string
        elif len(cmd_args) > 1:
            print("Error: Too many arguments.")
            return string
        
        exec_cmd = cmd_args[0].strip()

        if len(exec_cmd) > 1:
            exec_file = exec_cmd[1]
            exec_file = os.path.expanduser(exec_file)
            if os.path.exists(exec_file):
                exec_cmd[1] = exec_file

        print(f"Executing: `{exec_cmd}`...\n")
        # Run the command and capture output
        result = subprocess.run(exec_cmd.split(" "), capture_output=True, text=True)

        # Get the standard output as a string
        
        cmd_stdout = result.stdout
        cmd_stderr = result.stderr

        insert_string = f"\nCMD Out:\n```bash\n{cmd_stdout}\n```\nCMD Err::\n```bash\n{cmd_stderr}\n```"
        print(insert_string)
        print('\n')


        output = self._remove_substring(string, start, arg_end)
        output = self._insert_substring(output, insert_string, start)

        end_index = start + len(insert_string)

        return output, end_index
    


        

        
