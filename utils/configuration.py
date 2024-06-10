import yaml
from colorama import Fore, Style

def get_token():
    try:
        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['token']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.yml not found!{Style.RESET_ALL}")
        exit(1)

def get_channel_ids():
    try:
        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['channel_ids']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.yml not found!{Style.RESET_ALL}")
        exit(1)
    
def get_characterai_token():
    try:
        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['character_ai_token']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.yml not found!{Style.RESET_ALL}")
        exit(1)

def get_characterai_character_id():
    try:
        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config['character_ai_character_id']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.yml not found!{Style.RESET_ALL}")
        exit(1)