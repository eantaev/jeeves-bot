#!/usr/bin/env python3

import argparse

import psutil

from jeeves import *


def start(bot, update):
    print('started new chat ', update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text='Hi, I am Jeeves')


def message_callback(bot, update):
    print('received message in chat', update.message.chat_id, update.message.text)
    if update.message.chat_id == CHAT_ID:
        bot.send_message(chat_id=update.message.chat_id, text='yeah')
    else:
        bot.send_message(chat_id=update.message.chat_id, text="you're not Wooster")


def heartbeat(bot, job):
    bot.send_message(chat_id=CHAT_ID, text='.')
    logging.log(logging.INFO, msg='sent heartbeat')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--silent-start', dest='silent_start', action='store_const', const=True, default=False)
    args = parser.parse_args()

    own_pid = os.getpid()
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if own_pid != pid and Jeeves.is_jeeves_process(p):
            if not args.silent_start:
                print('Process %s (PID=%d) is already running (%s)' % (PROCESS_NAME, pid, p.cmdline()))
            exit()

    print('Starting..')
    print('PID =', own_pid)

    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO)

    j = Jeeves()

    print('Started')

    j.idle()


if __name__ == '__main__':
    main()
