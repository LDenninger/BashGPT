import argparse
import json
import os

from src.BashGPT import BashGPT
from src.models.ChatGPT import ChatGPT


            
if __name__ == '__main__':
    with open('resources/config.json', 'r') as f:
        config = json.load(f)
    if len(config['OPENAI_API_KEY']) == 0:
        if "OPENAI_API_KEY" not in os.environ:
            raise Exception('OPENAI_API_KEY not set in config.json or in environment variable OPENAI_API_KEY')
        config['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']

    system_calls = {key.lower(): value for key, value in config['SYSTEM_CALLS'].items()}

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default=config['MODEL_NAME'], help='The name of the model to use')
    parser.add_argument('--chat_name', type=str, default=config['CHAT_NAME'], help='The name of the chat to use or load')
    parser.add_argument('--mode', type=str, default=config['MODE'], help='The mode of the chat determining the system call.')
    parser.add_argument('--temperature', type=float, default=config['TEMPERATURE'], help='temperature of the model defining the randomness')
    parser.add_argument('--max_tokens', type=int, default=config['MAX_TOKENS'], help='Maximal number of tokens to generate')
    parser.add_argument('--use_past', type=bool, default=config['USE_PAST'], help='Whether to use the past messages which might lead to explosion of token usage')
    parser.add_argument('--top_p', type=bool, default=config['TOP_P'], help='Whether to output multiple top-p responses')
    parser.add_argument('--ram', action='store_true', default=config['KEEP_IN_RAM'], help='Whether to output multiple top-p responses')
    args = parser.parse_args()



    chat_gpt = ChatGPT( model_name = args.model_name, 
                        temperature = args.temperature, 
                        max_tokens = args.max_tokens, 
                        top_p = args.top_p,
                        api_key = config['OPENAI_API_KEY']
    )
    

    bash_gpt = BashGPT(
        chat_model=chat_gpt,
        chat_name=args.chat_name,
        keep_in_ram=args.ram
    )

    while True:
        try:
            bash_gpt()
        except KeyboardInterrupt:
            break
    
