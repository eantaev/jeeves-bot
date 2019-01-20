import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import camera

TOKEN = "" # todo fill
CHAT_ID = 0
PROCESS_NAME = 'jeeves'
HEARTBEAT_INTERVAL_SEC = 30 * 60


class Jeeves:
    def __init__(self):
        self.updater = Updater(token=TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot

        print(self.bot.get_me())

        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('suspend', self.suspend_heartbeats))
        self.dispatcher.add_handler(CommandHandler('resume', self.resume_heartbeats))
        self.dispatcher.add_handler(CommandHandler('shutdown', self.shutdown))
        self.dispatcher.add_handler(CommandHandler('photo', self.take_photo))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_callback))

        self.job_queue = self.updater.job_queue
        self.heartbeats_job = None
        self.resume_heartbeats()

        self.updater.start_polling(read_latency=5)

    def idle(self):
        try:
            self.updater.idle()
        finally:
            print('Stopping..')
            self.updater.stop()

    def start(self, bot, update):
        print('started new chat ', update.message.chat_id)
        if update.message.chat_id != CHAT_ID:
            return
        bot.send_message(chat_id=update.message.chat_id, text='Hi, I am Jeeves')

    def message_callback(self, bot, update):
        print('received message in chat', update.message.chat_id, update.message.text)
        if update.message.chat_id != CHAT_ID:
            return
        if update.message.chat_id == CHAT_ID:
            bot.send_message(chat_id=update.message.chat_id, text='ok')
        else:
            bot.send_message(chat_id=update.message.chat_id, text="you're not Wooster")

    def suspend_heartbeats(self, bot, update):
        if update.message.chat_id != CHAT_ID:
            return
        if self.heartbeats_job:
            self.heartbeats_job.enabled = False
            self.heartbeats_job.schedule_removal()
            self.heartbeats_job = None
            logging.log(logging.INFO, msg='suspended')

    def resume_heartbeats(self, bot=None, update=None):
        if update and update.message.chat_id != CHAT_ID:
            return
        if not self.heartbeats_job:
            self.heartbeats_job = self.job_queue.run_repeating(self.heartbeat, interval=HEARTBEAT_INTERVAL_SEC, first=0)
            logging.log(logging.INFO, msg='resumed')

    def heartbeat(self, bot, job):
        bot.send_message(chat_id=CHAT_ID, text='.')
        logging.log(logging.INFO, msg='sent heartbeat')

    def take_photo(self, bot, update):
        if update.message.chat_id != CHAT_ID:
            return
        try:
            image_file = camera.take_photo()
            if image_file:
                with open(image_file, 'rb') as photo:
                    bot.send_photo(chat_id=update.message.chat_id, photo=photo)
            else:
                bot.send_message(chat_id=update.message.chat_id, text='no camera')
        except Exception as e:
            bot.send_message(chat_id=update.message.chat_id, text=str(e))

    def shutdown(self, bot, update):
        if update.message.chat_id != CHAT_ID:
            return
        logging.warning('shutting down..')
        self.job_queue.run_once(self.kill, when=5)

    def kill(self, bot, job):
        os._exit(0)

    @staticmethod
    def is_jeeves_process(process):
        if 'python' in process.name():
            for param in process.cmdline():
                if PROCESS_NAME in param:
                    return True
        return False
