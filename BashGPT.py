import argparse
import json

from src.Printer import SimpleBash
from src.ChatGPT import ChatGPT


            
if __name__ == '__main__':
    with open('resources/config.json', 'r') as f:
        config = json.load(f)

    system_calls = {key.lower(): value for key, value in config['SYSTEM_CALLS'].items()}

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default=config['MODEL_NAME'], help='The name of the model to use')
    parser.add_argument('--mode', type=str, default=config['MODE'], help='The mode of the chat determining the system call.')
    parser.add_argument('--temperature', type=float, default=config['TEMPERATURE'], help='temperature of the model defining the randomness')
    parser.add_argument('--max_tokens', type=int, default=config['MAX_TOKENS'], help='Maximal number of tokens to generate')
    parser.add_argument('--use_past', type=bool, default=config['USE_PAST'], help='Whether to use the past messages which might lead to explosion of token usage')
    parser.add_argument('--top_p', type=bool, default=config['TOP_P'], help='Whether to output multiple top-p responses')
    args = parser.parse_args()



    chat_gpt = ChatGPT(args.model_name, system_calls,
                        args.mode, args.temperature, 
                        args.max_tokens, args.top_p, config['OPENAI_API_KEY'])
    

    printer = SimpleBash()

    while True:
        try:
            user_input = printer.request_input()
            if user_input == 'exit':
                break
            else:
                response = chat_gpt(user_input, use_past=args.use_past)
                printer.print(chat_gpt.get_messages())
        except KeyboardInterrupt:
            break
    
