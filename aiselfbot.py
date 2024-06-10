import discum
import asyncio
import time
import utils.configuration as config
import os
import threading
from characterai import aiocai
from colorama import Fore, Style

bot = discum.Client(token=config.get_token(), log=False)
typing = False


def get_chat_id():
    chat_id_file = "chat_id.txt"
    if os.path.exists(chat_id_file):
        with open(chat_id_file, "r") as f:
            chat_id = f.read().strip()
            return chat_id
    return None


def save_chat_id(chat_id):
    chat_id_file = "chat_id.txt"
    with open(chat_id_file, "w") as f:
        f.write(chat_id)
    print(f"{Fore.GREEN}► Chat Created: {chat_id} {Style.RESET_ALL}")


async def get_characterai_response(message_content, chat_id):
    client_ai = aiocai.Client(config.get_characterai_token())
    me = await client_ai.get_me()

    async with await client_ai.connect() as chat:
        if chat_id:
            response = await chat.send_message(config.get_characterai_character_id(), chat_id, message_content)
        else:
            new, answer = await chat.new_chat(config.get_characterai_character_id(), me.id)
            save_chat_id(new.chat_id)
            response = await chat.send_message(config.get_characterai_character_id(), new.chat_id, message_content)
        return response.text


@bot.gateway.command
def onReady(response):
    if response.event.ready_supplemental:
        user = bot.gateway.session.user
        print(f"{Fore.GREEN}► Logged in as: {user['username']} [{user['id']}]{Style.RESET_ALL}")


@bot.gateway.command
def onMessage(response):
    global typing
    if response.event.message:
        user = bot.gateway.session.user
        message = response.parsed.auto()
        message_id = message['id']
        author_username = message['author']['username']
        channel_id = message['channel_id']
        message_content = message['content']

        if config.get_channel_ids() and channel_id not in config.get_channel_ids():
            return
        if message['author']['id'] == user['id']:
            return
        
        typing = True
        typing_thread = threading.Thread(target=typing_action, args=(channel_id,))
        typing_thread.start()

        chat_id = get_chat_id()
        response = asyncio.run(get_characterai_response(message_content, chat_id))
        if response is None:
            print(f"{Fore.RED}► Error: No response from CharacterAI{Style.RESET_ALL}")
            bot.reply(channel_id, message_id, "An error occurred in my programming. Please try again later.")
            return

        bot.reply(channel_id, message_id, response)
        print(f"{Fore.GREEN}{author_username} ► {response} {Style.RESET_ALL}")
        typing = False


def typing_action(channel_id):
    global typing
    while typing:
        bot.typingAction(channel_id) # Typing action (realistic)
        time.sleep(5)


bot.gateway.run(auto_reconnect=True)