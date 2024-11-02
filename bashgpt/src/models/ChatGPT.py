from enum import Enum
import openai
from typing import Dict
import json

from functions import FunctionTemplate
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

        self.tools = {}
        self.tool_descs = []
    
    def __call__(self, messages: Dict[str,str]):

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            functions=self.tool_descs,
            function_call="auto"
        )

        response = response.choices[0]
        if response.finish_reason == 'function_call':
            func_args = json.loads(response.message.function_call.arguments)
            func = self.tools[response.message.function_call.name]
            func_response = func(**func_args)
            if func_response is not None:
                messages.append(message_template("user", func_response))
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                )
                response = response.choices[0]

        response_message = response.message.content
        return response_message
        
    def add_tool(self, tool: FunctionTemplate):
        self.tools[tool.__class__.__name__] = tool
        self.tool_descs.append(tool.get_description())




