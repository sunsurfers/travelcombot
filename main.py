#!/usr/bin/env python3

import os
import time
import logging

import telebot
from telebot import types, apihelper

import database
import texts
import config


logging.basicConfig(filename=config.LOGGER_PATH, level=logging.INFO)

bot = telebot.TeleBot(config.BOT_TOKEN)


# Обработчики последовательных действий пользователей 
READY_TO_REGISTER = {}  # Регистрация
READY_TO_ADMIN_EMAIL = {}  # Рассылка сообщения админом


@bot.message_handler(commands=['start'])
def start_command_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	user = database.get_user(uid)
	if not user:
		logging.info('Started by {!s}, id {!s}'.format(message.from_user.first_name, cid))
		READY_TO_REGISTER[uid] = {}
		markup = types.ReplyKeyboardRemove()
		return bot.send_message(cid, texts.start_text, reply_markup=markup)
	if not user['is_confirm']:
		return bot.send_message(cid, texts.wait_confirm_text)
	# TODO: Выдача основного меню пользователя.
	return bot.send_message(cid, 'В разработке...')


@bot.message_handler(commands=['admin'])
def admin_command_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	
	if uid not in config.ADMINS:
		return bot.send_message(cid, texts.admin_access_denied_text)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
	for x in config.admin_markup:
		markup.add(x)
	return bot.send_message(cid, texts.admin_panel_greet_text, reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def text_content_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	# Обработка добавления аватарки
	if uid in READY_TO_REGISTER:
		if 'avatar' not in READY_TO_REGISTER[uid]:
			file_info = bot.get_file(message.photo[-1].file_id)
			downloaded_file = bot.download_file(file_info.file_path)
			photo_path = '{!s}{!s}.jpg'.format(config.AVARATRS_PATH, uid)
			with open(photo_path, 'wb') as new_file:
				new_file.write(downloaded_file)
			READY_TO_REGISTER[uid]['avatar'] = photo_path
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			for x in config.community_types:
				markup.add(x)
			markup.add('Другое')
			return bot.send_message(cid, texts.register_travel_type, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_content_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	# Обработка первой регистрации пользователя в боте
	if uid in READY_TO_REGISTER:
		if 'name' not in READY_TO_REGISTER[uid]:
			READY_TO_REGISTER[uid]['name'] = message.text
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
			markup.row('Не сейчас')
			return bot.send_message(cid, texts.add_avatar_text, reply_markup=markup)
		elif 'avatar' not in READY_TO_REGISTER[uid]:
			if message.text == 'Не сейчас':
				READY_TO_REGISTER[uid]['avatar'] = 'default.jpg'
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
				for x in config.community_types:
					markup.add(x)
				markup.add('Другое')
				return bot.send_message(cid, texts.register_travel_type, reply_markup=markup)
			return bot.send_message(cid, texts.error_avatar_text)
		elif 'community' not in READY_TO_REGISTER[uid]:
			if message.text == 'Другое':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton('Узнать, кто такие сансерферы', url='https://sunsurfers.ru'))
				keyboard.add(types.InlineKeyboardButton('Узнать, кто такие сменщики', url='https://smenastation.com'))
				return bot.send_message(cid, texts.community_more_info_text, reply_markup=keyboard)
			if message.text not in config.community_types:
				return bot.send_message(cid, texts.error_button_text)
			READY_TO_REGISTER[uid]['community'] = message.text

			# TODO: автоматическая проверка на присутсивие в white листе airtables
			if READY_TO_REGISTER[uid]['community'] == 'Сансерферы':
				pass
			
			markup = types.ReplyKeyboardRemove()
			return bot.send_message(cid, texts.register_events_question_text, reply_markup=markup)
		elif 'events' not in READY_TO_REGISTER[uid]:
			READY_TO_REGISTER[uid]['events'] = message.text
			return bot.send_message(cid, texts.register_confirm_people_text)
		elif 'confirm_people' not in READY_TO_REGISTER[uid]:
			READY_TO_REGISTER[uid]['confirm_people'] = message.text

			user = database.add_user(uid, int(time.time()), READY_TO_REGISTER[uid]['name'], 
				READY_TO_REGISTER[uid]['avatar'], READY_TO_REGISTER[uid]['community'],
				READY_TO_REGISTER[uid]['events'], READY_TO_REGISTER[uid]['confirm_people'], None, 0)

			# Отправить анкету в канал админов
			channel_text = 'Новая заявка №{!s}\n\n<a href="tg://user?id={!s}">Ссылка</a>\n\nИмя: {!s}\nСообщество: {!s}\nМероприятия: {!s}\nДоверенные люди: {!s}'.format(
				user['id'], uid, READY_TO_REGISTER[uid]['name'], READY_TO_REGISTER[uid]['community'], 
				READY_TO_REGISTER[uid]['events'], READY_TO_REGISTER[uid]['confirm_people'])
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirmanket_{!s}_{!s}'.format(user['id'], user['uid'])))
			keyboard.add(types.InlineKeyboardButton('❌ Отклонить', callback_data='refuseanket_{!s}_{!s}'.format(user['id'], user['uid'])))
			bot.send_photo(config.admin_channel_id, open(READY_TO_REGISTER[uid]['avatar'], 'rb'), 
				caption=channel_text, reply_markup=keyboard, parse_mode='HTML')

			logging.info('User {!s} anket sended to channel'.format(cid))

			del READY_TO_REGISTER[uid]
			markup = types.ReplyKeyboardRemove()
			return bot.send_message(cid, texts.register_complete, reply_markup=markup)
	
	# Обработка отмены действий админа
	if message.text == '❌ Отмена':
		if uid in config.ADMINS:
			if uid in READY_TO_ADMIN_EMAIL:
				del READY_TO_ADMIN_EMAIL[uid]
			bot.send_message(cid, texts.cancel_text)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			for x in config.admin_markup:
				markup.add(x)
			return bot.send_message(cid, texts.admin_panel_greet_text, reply_markup=markup)

	# Обработка действий админа
	if uid in READY_TO_ADMIN_EMAIL:
		if 'text' not in READY_TO_ADMIN_EMAIL[uid]:
			READY_TO_ADMIN_EMAIL[uid]['text'] = message.text
			logging.info('Admin message email')

			users = database.get_all_users()
			for x in users:
				try:
					bot.send_message(x['uid'], READY_TO_ADMIN_EMAIL[uid]['text'])
				except Exception as e:
					print(e)
					continue

			del READY_TO_ADMIN_EMAIL[uid]
			bot.send_message(cid, texts.success_send_email_admin_text)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			for x in config.admin_markup:
				markup.add(x)
			return bot.send_message(cid, texts.admin_panel_greet_text, reply_markup=markup)

	# Обработка админ-панели
	if uid in config.ADMINS:
		if message.text == 'Создать рассылку':
			READY_TO_ADMIN_EMAIL[uid] = {}
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			markup.add('❌ Отмена')
			return bot.send_message(cid, texts.ready_send_email_admin_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	cid = call.message.chat.id
	uid = call.from_user.id

	print(call.data)

	try:
		bot.answer_callback_query(call.id, '✅')
	except Exception as e:
		print(e)

	if call.data.startswith('confirmanket'):
		anket_id = int(call.data.split('_')[1])
		user_id = int(call.data.split('_')[2])
		database.confirm_user(anket_id)

		# Выслать уведомление пользователю
		try:
			bot.send_message(user_id, texts.success_confirm_anket_text)
		except Exception as e:
			print(e)

		text = 'Заявка подтверждена'
		return bot.edit_message_caption(text, chat_id=cid, message_id=call.message.message_id)
	elif call.data.startswith('refuseanket'):
		anket_id = int(call.data.split('_')[1])
		user_id = int(call.data.split('_')[2])
		database.delete_user(anket_id)

		# Выслать уведомление пользователю
		try:
			bot.send_message(user_id, texts.unsuccess_confirm_anket_text)
		except Exception as e:
			print(e)

		text = 'Заявка отклонена'
		return bot.edit_message_caption(text, chat_id=cid, message_id=call.message.message_id)


def main():
	database.create_tables()

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


if __name__ == '__main__':
	main()
