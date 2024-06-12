import os
import utils.configutils as config
from characterai import aiocai
from colorama import Fore, Style

def get_chat_id(channel_id):
    chat_id_file = channel_id + "_chat_id.txt"
    if os.path.exists(chat_id_file):
        with open(chat_id_file, "r") as f:
            chat_id = f.read().strip()
            return chat_id
    return None


def save_chat_id(channel_id, chat_id):
    chat_id_file = channel_id + "_chat_id.txt"
    with open(chat_id_file, "w") as f:
        f.write(chat_id)
    print(f"{Fore.GREEN}► Chat Created: {chat_id} [{channel_id}] {Style.RESET_ALL}")


async def get_characterai_response(channel_id, message_content, chat_id):
    client_ai = aiocai.Client(config.get_characterai_token())
    me = await client_ai.get_me()

    async with await client_ai.connect() as chat:
        if chat_id:
            response = await chat.send_message(config.get_characterai_character_id(), chat_id, message_content)
        else:
            new, answer = await chat.new_chat(config.get_characterai_character_id(), me.id)
            save_chat_id(channel_id, new.chat_id)
            response = await chat.send_message(config.get_characterai_character_id(), new.chat_id, message_content)
        return response.text