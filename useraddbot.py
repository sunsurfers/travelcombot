#!/usr/bin/env python3

import logging

import telebot

import database
import config

from main_func import main


logging.basicConfig(filename=config.LOGGER_PATH, level=logging.INFO)

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(content_types=['new_chat_members'])
def new_chat_member(message):
	communities = {i['chat_id']: i['id'] for i in database.get_communities()}
	for user in message.new_chat_members:
		if user.is_bot:
			logging.info('ignornig user#%d: is bot', user.id)
			continue
		if not user.username:
			logging.info('ignornig user#%d: no username', user.id)
			continue
		record = database.get_user(user.id)
		if record:
			continue
		logging.info('adding user#%d %s', user.id, user.username)
		database.add_user(
			email=None,
			name=user.username,
			photo='default.jpg',
			is_host=0,
			about=None,
			telegram=user.id,
			insta=None,
			community=communities[message.chat.id],
		)


if __name__ == '__main__':
	main(bot)
