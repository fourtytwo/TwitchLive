import asyncio
import aiohttp

from config.Configuration import Configuration


class Handle(object):
    """
    Class containing all the lists
    and is supposed to be run asyncronously.
    """


    def __init__(self , refresh=20 , top_games_c=10 , top_streamers_c=10 , featured_max=10 , games_count=10):
        """
        Handle Constructor
        :param refresh:
        :param top_streamers_c: Amount of top streamers being refreshed
        :param top_games_c: Amount of top games being refreshed
        """
        self.refresh = refresh
        self.games_max =games_count
        self.top_games = [[],(top_games_c)]
        self.top_streams = [[], top_streamers_c]
        self.featured = [[], featured_max]
        self.streams_by_game = {}

    async def update_games(self):
        payload = {'limit': self.top_games[1]}
        result_list = []
        with aiohttp.ClientSession() as session:
            link = '{}/games/top'.format(Configuration.config['api_base_link'])
            while True:
                res = await session.get(link, params = payload)
                json_result =  await res.json()
                for games_objects in json_result['top']:
                    result_list.append({'viewers' : games_objects['viewers'],
                        'name' : games_objects['game']['name'] ,
                        'channel_count' :games_objects['channels']})

                if len(result_list) < self.top_games[1] and len(result_list) < int(json_result['_total']):
                    link =json_result['_links']['next']
                else:
                    break

        self.top_games = (result_list , self.top_games[1])


    async def update_top_streams(self):
        payload = {'limit': self.top_streams[1]}
        result_list = []
        with aiohttp.ClientSession() as session:
            link = '{}/streams'.format(Configuration.config['api_base_link'])
            while True:
                res  = await session.get(link , params = payload)
                json_result = await res.json()
                for streams_objects in json_result['streams']:
                    result_list.append({'channel_name' : streams_objects['channel']['name'],
                                        'game': streams_objects['game'] ,
                                        'viewers' : streams_objects['viewers'] ,
                                        'url' : streams_objects['channel']['url'],
                                        'title' : streams_objects['channel']['status'] })

                if len(result_list) < self.top_streams[1] and len(result_list) < int(json_result['_total']):
                    link =json_result['_links']['next']
                else:
                    break

        self.top_streams = (result_list , self.top_streams[1])


    async def update_featured(self):
        payload = {'limit': self.featured[1]}
        result_list = []
        with aiohttp.ClientSession() as session:
            link = '{}/streams/featured'.format(Configuration.config['api_base_link'])
            while True:
                res = await session.get(link, params=payload)
                json_result = await res.json()
                for featured in json_result['featured']:
                    streams_objects = featured['stream']
                    result_list.append({'channel_name' : streams_objects['channel']['name'],
                                        'game': streams_objects['game'] ,
                                        'viewers' : streams_objects['viewers'] ,
                                        'url' : streams_objects['channel']['url'],
                                        'title' : streams_objects['channel']['status'] })

                if len(result_list) < self.top_streams[1] and len(result_list) < int(json_result['_total']):
                    link =json_result['_links']['next']
                else:
                    break

        self.featured = (result_list , self.featured[1])



    async def update(self):
        await self.update_games()
        await self.update_top_streams()
        await self.update_featured()

    async def run(self):
        while True:
            await self.update()
            print(self.top_streams)
            print(self.top_games)
            print(self.featured)
            await asyncio.sleep(self.refresh)