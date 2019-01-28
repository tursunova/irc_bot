from Bot import Bot

if __name__ == '__main__':

    options = {
        'server': 'chat.freenode.net',
        'port': 6667,
        'channel': '#2448',
        'nickname': 'FactsBot',
        'log_file': 'log.txt'
    }

    bot = Bot(**options)
    bot.connect()
    bot.listen()
