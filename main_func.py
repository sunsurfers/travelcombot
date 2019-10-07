import os
import time

from telebot import apihelper

import config


def main(bot):
	# Создать папку для хранения аватарок пользователей
	try:
		os.mkdir(config.AVARATRS_PATH)
	except Exception as e:
		pass

	if config.DEBUG:
		apihelper.proxy = config.PROXY
		bot.polling()
	else:
		while True:
			try:
				bot.polling(none_stop=True, interval=0)
			except Exception as e:
				print(e)
				time.sleep(30)
				continue
