#./usr/bin/python3
import os 
import sys; sys.path.insert(0,os.path.dirname(__file__))
import argparse
import json
from pathlib import Path

from utils.config import Config
from utils.chats import Chat, Profile, message_template
from models.ChatGPT import ChatGPT

from termcolor import colored

CONFIG_DIR = '/usr/share/bashgpt/config'
DEBUG = False

def arguments():

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ask', action="store_true", default=False, help="Ask ChatGPT")
    group.add_argument('--set', action="store_true", default=False, help="Set config variable")
    group.add_argument('--get_config', action="store_true", default=False, help="Get current configuration")

    parser.add_argument('--key', type=str, default=None, help="Key of the configuration variable to be set")
    parser.add_argument('--value', type=str, default=None, help="Value of the configuration variable to be set")

    parser.add_argument('--question', type=str, default=None, help="Question to be asked")

    parser.add_argument('--debug', action="store_true", default=DEBUG, help="Run BashGpt in debug mode.")


    args = parser.parse_args()

    if args.set and (args.key is None or args.value is None):
        print("Cannot set variable. Usage: gpt set [key] [value]")
        exit(-1)

    return args



def main():


    args = arguments()

    config_dir = Path(CONFIG_DIR)

    if args.debug:
        print("Running BashGPT in debug mode...")

    config = Config(str(config_dir/ "config.json"), True)
    if args.debug:
        print(config)


    if args.ask:

        if "OPENAI_API_KEY" not in os.environ:
            print("OPENAI_API_KEY not set in environment. Please set it before running BashGPT.")
            exit(-1)

        config.set_private_key("openai_api_key", os.getenv('OPENAI_API_KEY'))

        try:
            with open(config_dir / config["profile_path"]) as f:
                profiles = json.load(f)
        except FileNotFoundError:
            print(colored(f"ERROR: Profile path not found {config['profile_path']}", "red"))
            exit(-1)
    
        profile_objs = {}
        for k, v in profiles.items():
            profile_dict = v
            profile_dict.update({"name": k})
            profile_objs[k] = Profile(profile_dict)
        profiles = profile_objs

        #profiles = [Profile(v.update({"name": k})) for k, v in profiles.items()]
        if config["profile"] in str(profiles.keys()):
            profile = profiles[config["profile"]]
        else:
            print(colored(f"WARNING: Profile {config['profile']} not found, falling back to default!", "orange"))
            profile = profiles[0]

        base_prompt = profile.get_prompt()
        messages = base_prompt + [message_template('user', args.question)]

        chat_gpt = ChatGPT( model_name = config["model_config"]['name'], 
            temperature = config["model_config"]['temperature'], 
            max_tokens = config["model_config"]['max_tokens'], 
            top_p = config["model_config"]['top_p'],
            api_key = config["openai_api_key"]
        )

        response = chat_gpt(messages)
        print(response)

    if args.set:
        config[args.key] = args.value

        if args.debug:
            print(f"Setting {args.key} -> {args.value}")
            print(config)

        config.save()

        




if __name__ == "__main__":
    main()

