from enum import Enum
import openai
from typing import Dict

from .ModelInterface import ModelInterface

message_template = lambda role, message: {'role': role, 'content': message}

PYTHON_SYSTEM_CALL = "You are a helpful assistant answering coding questions in python. Please exclude comments and any explanations in your response."
CPP_SYSTEM_CALL = "You are a helpful assistant answering coding questions in C++. Please exclude comments within the code."
LATEX_SYSTEM_CALL = "You are a helpful assistant answering questions about latex and giving correct latex formatted equations. Please exclude comments within the code."
ASSISTANT_SYSTEM_CALL = "You are a helpful assistant."
COMMAND_LINE_SYSTEM_CALL = ""

prompt_map = {
    'python': PYTHON_SYSTEM_CALL,
    'cpp': CPP_SYSTEM_CALL,
    'latex': LATEX_SYSTEM_CALL,
    'assistant': ASSISTANT_SYSTEM_CALL,
}


class ChatGPT(ModelInterface):
    def __init__(self,
                 model_name: str,
                 temperature:float=0.0,
                 max_tokens: int=300,
                 top_p: float=1.0,
                 api_key: str=None
                 ):
        ##-- Parameters --##
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

        self.client = openai.OpenAI(api_key=api_key)
    
    def __call__(self, messages: Dict[str,str]):
    
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
        )
        response_message = response.choices[0].message.content

        return response_message
       



