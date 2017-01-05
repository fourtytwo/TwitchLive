import aiohttp
import requests
import pprint
import asyncio
from model import handle

from config.Configuration import Configuration

""" Returns List Containing Dictionary with name, viewers, channel_count

"""

async def get_games(amount=10, offset=0):

    payload = {'limit': amount,'offset':offset}
    games = []
    with aiohttp.ClientSession() as session:
        r = await session.get('https://api.twitch.tv/kraken/games/top', params = payload)
        for games_objects in (await r.json())['top']:
         games.append({'viewers' : games_objects['viewers'],
                        'name' : games_objects['game']['name'] ,
                       'channel_count' :games_objects['channels']})
    return games

def list_games( list):
    print('{:<3}|{:<40}|{:<15}|{:<10}|'.format('#' , 'Game' , 'Channels' , 'Viewers'))
    for index , e  in enumerate(list):
        print('{:<3'
              '}|{:-<40}{:-<15}{:-<10}|'.format(index , e['name'] , e['channel_count'] , e['viewers']))



async def get_streams(game=None , amount=None, offset=None):

    payload = {'game' : game , 'limit': amount , 'offset':offset}
    with aiohttp.ClientSession() as session:
        r = await session.get('https://api.twitch.tv/kraken/streams', params = payload)
        pprint.pprint(await r.json())


#def list_streams():


def main():
    current_list=[]
    index = 0
    while True:
        inp = input('>')
        if inp == 'lg' or inp == 'list games':
            loop=asyncio.get_event_loop()
            current_list = (loop.run_until_complete(get_games()))
            list_games(current_list)
        if inp.startswith('open') or inp.startswith('o'):
            try:
                num = int(inp.split(' ')[1])
            except Exception as e:
                print("Sorry you need to input the number you want opened")
                continue

            print("opening {}".format(current_list[num]['name']))
            loop=asyncio.get_event_loop()
            list =loop.run_until_complete(get_streams(game=current_list[num]['name']))

        if inp == 'e' or inp == 'exit':
            return

    payload = {'game' : 'Counter-Strike: Global Offensive' , 'limit':10, }
    r = requests.get('https://api.twitch.tv/kraken/streams' , params=payload)




if __name__ == '__main__':
    Configuration.load()
    loop=asyncio.get_event_loop()
    loop.run_until_complete(handle.Handle(refresh=1, top_games_c=5).run())
