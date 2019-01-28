import socket
import threading
import time
import urllib3
from os.path import exists, join
from random import randint


class Bot:
    init_message = 'do some magic'
    exit_message = 'bye'

    def __init__(self, server, port, channel, nickname, log_file):
        self.server_ = server
        self.port_ = port
        self.channel_ = channel
        self.nickname_ = nickname
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log_file_ = log_file
        self.http = urllib3.PoolManager()
        open(self.log_file_, 'w').close()

    def send_message(self, message, privmsg=True):
        if privmsg:
            message = 'PRIVMSG {} :{}\r\n'.format(self.channel_, message)
            print('<{}>: {}'.format(self.nickname_, message))
        self.irc.send(message.encode('utf-8'))

    def connect(self):
        self.irc.connect((self.server_, self.port_))
        self.send_message('USER {} * * : !\n'.format(self.nickname_), False)
        self.send_message('NICK {}\n'.format(self.nickname_), False)
        self.send_message('JOIN {}\n'.format(self.channel_), False)

    def get_message(self):
        result = self.irc.recv(1024).decode('utf-8')
        return result

    def listen(self):
        threads = []
        while True:
            recieve = self.get_message()
            if 'PING' in recieve:
                response = recieve.split(' ')[1]
                if response == '001':
                    self.send_message('JOIN {}\n'.format(self.channel_), False)
                else:
                    self.send_message('PONG {}\n'.format(recieve.split(' ')[1]), False)
            else:
                with open(self.log_file_, 'a') as log:
                    log.write(recieve + '\n')
                if 'PRIVMSG' in recieve and 'VERSION' not in recieve:
                    author, message = self.parse_recieve_privmsg(recieve)
                    print('<{}>: {}'.format(author, message))
                    if message.find(self.nickname_) != -1 and message.find(self.init_message) != -1:
                        thread = threading.Thread(target=self.show_fact)
                        thread.start()
                        threads.append(thread)
                    elif message.find(self.nickname_) != -1 and message.find(self.exit_message) != -1:
                        self.send_message(self.exit_message)
                        break
        for thread in threads:
            thread.join()

    def parse_recieve_privmsg(self, recieve):
        author = recieve.split('!')[0][1:]
        message = ':'.join(recieve.split(':')[2:])
        if '\r\n' == message[-2:]:
            message = message[:-2]
        return author, message

    def show_fact(self):
        lst = []
        file = open("facts", "r")
        for line in file:
            lst.insert(0, line)
        num = randint(0, 104)
        self.send_message(lst[num])
        print('<{}>: {}'.format(self.nickname_, lst[num]))
        time.sleep(0.5)