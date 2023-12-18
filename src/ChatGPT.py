from enum import Enum
import openai

message_template = lambda role, message: {'role': role, 'content': message}

PYTHON_SYSTEM_CALL = "You are a helpful assistant answering coding questions in python. Please exclude comments within the code."
CPP_SYSTEM_CALL = "You are a helpful assistant answering coding questions in C++. Please exclude comments within the code."
LATEX_SYSTEM_CALL = "You are a helpful assistant answering questions about latex and giving correct latex formatted equations. Please exclude comments within the code."
ASSISTANT_SYSTEM_CALL = "You are a helpful assistant."
COMMAND_LINE_SYSTEM_CALL = " Please provide the code output with correct indentation using '\t' and '\n' such that it can be printed in a command line."

prompt_map = {
    'python': PYTHON_SYSTEM_CALL,
    'cpp': CPP_SYSTEM_CALL,
    'latex': LATEX_SYSTEM_CALL,
    'assistant': ASSISTANT_SYSTEM_CALL,
}

class ChatGPT:
    def __init__(self,
                 model_name: str,
                 mode:str='assistant',
                 temperature:float=0.0,
                 max_tokens: int=300,
                 api_key: str=None):
        ##-- Parameters --##
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.past_messages = []
        self.client = openai.OpenAI(api_key=api_key)
        self.mode = mode
    
    def __call__(self, 
                 message: str, 
                 mode:str=None, 
                 use_past:bool=True, 
                 cmd_line: bool=False):
        assert mode in ['python', 'cpp', 'latex', 'assistant', None], 'Please provide a valid mode for the chat completion'
        mode = mode if mode else self.mode
        # Build message query from the parameters
        message_query = [message_template('system', prompt_map[mode])]
        if cmd_line:
            message_query[0]['content'] += COMMAND_LINE_SYSTEM_CALL
        if use_past:
            message_query += self.past_messages
        # Append new message to the query
        new_message = message_template('user', message)
        message_query.append(new_message)
        self.past_messages.append(new_message)
        # Get the response from ChatGPT
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message_query,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1.0,
        )
        response_message = response.choices[0].message.content
        last_message = message_template('assistant', response_message)
        self.past_messages.append(last_message)

        return response_message

    def clear(self):
        self.past_messages = []

    def get_messages(self):
        return self.past_messages
       



