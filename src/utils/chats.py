from typing import *

from termcolor import colored


def message_template(role:str, content:str):
    return {"role": role, "content": content}

def format_chat(messages: List[dict]):

    role_print = {
        "user": colored("User: ", "red"),
        "assistant": colored("Assistant: ", "green"),
        "system": colored("System: ", "blue")
    }
    output_str = ""
    for message in messages:
        output_str += f"{role_print[message['role']]}\n{message['content']}"

    return output_str


class Chat:

    def __init__(self, messages):
        self.messages = messages

    def __call__(self):
        return self.messages

    def __str__(self):
        return format_chat(self.messages)
    

class Profile:
    def __init__(self, profile: dict):

        assert "system_call" in list(profile.keys()), "No system call provided in profile!"

        self.name = profile['name']
        self.system_call = profile["system_call"]
        self.chat = Chat(profile['messages'])

    def get_prompt(self):
        return [message_template('system', self.system_call)] + self.chat()

    