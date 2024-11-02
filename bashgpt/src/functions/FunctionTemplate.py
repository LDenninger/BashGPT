from abc import abstractmethod

class FunctionTemplate:
    """
    name:str = "template_function"
    description:str = "A template function to be implemented by their subclasses"
    parameters:dict = {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The customer's order ID.",
            },
        },
        "required": ["order_id"],
        "additionalProperties": False,
    }
    """


    def __init__(self, name:str, description:str, parameters:dict):
        self.name = name
        self.description = description
        self.parameters = parameters
        return
    
    @abstractmethod
    def __call__(self, ):
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def to_prompt(self, ):
        raise NotImplementedError("Subclasses must implement this method.")
        
    def get_description(self,):

        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    


