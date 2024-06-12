import discum
import asyncio
import time
import threading
from colorama import Fore, Style

import utils.configutils as config
import utils.chatutils as chatutils

bot = discum.Client(token=config.get_token(), log=False)
typing = False


@bot.gateway.command
def onReady(response):
    if response.event.ready_supplemental:
        user = bot.gateway.session.user
        print(f"{Fore.GREEN}► Logged in as: {user['username']} [{user['id']}]{Style.RESET_ALL}")


@bot.gateway.command
def onMessage(response):
    try:
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
            
            chat_id = chatutils.get_chat_id(channel_id)
            response = asyncio.run(chatutils.get_characterai_response(channel_id, message_content, chat_id))
            if response is None:
                print(f"{Fore.RED}► Error: No response from CharacterAI{Style.RESET_ALL}")
                bot.reply(channel_id, message_id, "An error occurred in my programming. Please try again later.")
                return
            
            bot.reply(channel_id, message_id, response)
            print(f"{Fore.GREEN}{author_username} ► {response} {Style.RESET_ALL}")
            typing = False
    except Exception as e:
        print(f"{Fore.RED}► Error: {e} {Style.RESET_ALL}")


def typing_action(channel_id):
    global typing
    while typing:
        bot.typingAction(channel_id) # Typing action (realistic)
        time.sleep(5)


bot.gateway.run(auto_reconnect=True)