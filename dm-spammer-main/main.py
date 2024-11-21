import requests
import colorama
import os
import pystyle
import asyncio
from colorama import *
from pystyle import *

os.system("cls")

logo = """
▓█████▄  ███▄ ▄███▓     ██████  ██▓███   ▄▄▄       ███▄ ▄███▓ ███▄ ▄███▓▓█████  ██▀███  
▒██▀ ██▌▓██▒▀█▀ ██▒   ▒██    ▒ ▓██░  ██▒▒████▄    ▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▓█   ▀ ▓██ ▒ ██▒
░██   █▌▓██    ▓██░   ░ ▓██▄   ▓██░ ██▓▒▒██  ▀█▄  ▓██    ▓██░▓██    ▓██░▒███   ▓██ ░▄█ ▒
░▓█▄   ▌▒██    ▒██      ▒   ██▒▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██    ▒██ ▒██    ▒██ ▒▓█  ▄ ▒██▀▀█▄  
░▒████▓ ▒██▒   ░██▒   ▒██████▒▒▒██▒ ░  ░ ▓█   ▓██▒▒██▒   ░██▒▒██▒   ░██▒░▒████▒░██▓ ▒██▒
 ▒▒▓  ▒ ░ ▒░   ░  ░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ▒░   ░  ░░ ▒░   ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒  ▒ ░  ░      ░   ░ ░▒  ░ ░░▒ ░       ▒   ▒▒ ░░  ░      ░░  ░      ░ ░ ░  ░  ░▒ ░ ▒░
 ░ ░  ░ ░      ░      ░  ░  ░  ░░         ░   ▒   ░      ░   ░      ░      ░     ░░   ░ 
   ░           ░            ░                 ░  ░       ░          ░      ░  ░   ░     
 ░                                                                                       
"""

class DmSpammer:
    def __init__(self, tokens):
        colorama.init()
        self.tokens = tokens

    async def Send(self, message, userid, token):
        url = f'https://discord.com/api/v10/users/@me/channels'
        headers = {'Authorization': f'Bot {token}'}

        payload = {'recipient_id': userid}
        r = requests.post(url=url, headers=headers, json=payload)

        if r.status_code == 200:
            channel_id = r.json()['id']
            print(Fore.GREEN + f"DM channel created: {channel_id}")
            
            message_url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
            message_payload = {'content': message}
            message_response = requests.post(url=message_url, headers=headers, json=message_payload)

            if message_response.status_code in [200, 201, 202, 203, 204]:
                print(Fore.GREEN + f"[+] Sent message through {token}")
            elif message_response.status_code == 429:
                print(Fore.YELLOW + f'[!] Ratelimited with {token}')
            else:
                print(Fore.RED + f"[-] Failed to send message with {token} {message_response.status_code}")
                print(Fore.RED + f"[-] Response :{message_response.text}")
        else:
            print(Fore.RED + f"[-] Failed to create DM with {token} {r.status_code}")
            print(Fore.RED + f"[-] Response :{r.text}")

    async def Start(self):
        message = input(Fore.BLUE + "Enter the message: ")
        user_id = input(Fore.BLUE + "Enter the user ID: ")

        while True:
            tasks = [self.Send(message, user_id, token) for token in self.tokens]  
            await asyncio.gather(*tasks) 


    async def Run(self):
        print(Colorate.Vertical(Colors.blue_to_red, Center.XCenter(logo)))
        sc = input(Fore.BLUE + f"1 Dm Spammer \n2 Exit \n \nselected choice: ")
        if sc == '1':
            await self.Start()
        else:
            print(Fore.RED + "Exiting")
            exit(1)

def load_tokens():
    with open("input/tokens.txt", "r") as f:
        return f.read().splitlines()

if __name__ == "__main__":
    tokens = load_tokens()
    spammer = DmSpammer(tokens)
    asyncio.run(spammer.Run())
