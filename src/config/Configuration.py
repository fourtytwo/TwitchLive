


class Configuration(object):
    config={}

    def __str__(self):
        return str(Configuration.config)

    @staticmethod
    def defaults():
        Configuration.config['api_base_link'] = 'https://api.twitch.tv/kraken/'

    @staticmethod
    def load(file=None):
        if file:
            with open (file, 'r', encoding='utf-8') as fh:
                Configuration.config['api_base_link'] = 'https://api.twitch.tv/kraken/'
        else:
            Configuration.defaults()
