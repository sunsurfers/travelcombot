#!/usr/bin/env python3

import uuid
import logging
import datetime

import telebot
from telebot import types

import database
import config
import texts
import util
from main_func import main


logging.basicConfig(filename=config.LOGGER_PATH, level=logging.INFO)

bot = telebot.TeleBot(config.BOT_TOKEN)


# Обработчики последовательных действий пользователей 
READY_TO_REGISTER = {}  # Регистрация
READY_TO_ADMIN_EMAIL = {}  # Рассылка сообщения админом
READY_TO_ADD_ABOUT = {}  # Добавление about
READY_TO_ADD_INSTA = {}  # Добавление insta
READY_TO_SHARE_LOCATION = {}  # Шеринг геопозиции


@bot.message_handler(commands=['start'])
def start_command_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	user = database.get_user(uid)

	# Проверка на регистрацию пользователя в боте
	if not user:
		logging.info('Started by {!s}, id {!s}'.format(message.from_user.first_name, cid))
		READY_TO_REGISTER[uid] = {}
		markup = types.ReplyKeyboardRemove()
		return bot.send_message(cid, texts.start_text, reply_markup=markup)

	# Проверка на подтвержденность анкеты админом
	if not user['is_host']:
		return bot.send_message(cid, texts.wait_confirm_text)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
	for x in config.main_markup:
		markup.row(x)
	return bot.send_message(cid, texts.main_text, reply_markup=markup)


@bot.message_handler(commands=['admin'])
def admin_command_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	
	# Проверка наличия прав админа
	if uid not in config.ADMINS:
		return bot.send_message(cid, texts.admin_access_denied_text)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
	for x in config.admin_markup:
		markup.add(x)
	return bot.send_message(cid, texts.admin_panel_greet_text, reply_markup=markup)


@bot.message_handler(content_types=['location'])
def location_content_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	# Проверка на регистрацию прользователя
	user = database.get_user(uid)
	if not user:
		markup = types.ReplyKeyboardRemove()
		return bot.send_message(cid, texts.register_invite_text, reply_markup=markup)

	# Обработка шеринга геопозиции
	if uid in READY_TO_SHARE_LOCATION:
		logging.info('User {!s} shared location'.format(cid))
		coordinates = '{!s} {!s}'.format(message.location.longitude, message.location.latitude) 
		database.add_visited_place(user['id'], coordinates, '', datetime.datetime.now())
		del READY_TO_SHARE_LOCATION[uid]
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		for x in config.main_markup:
			markup.row(x)
		return bot.send_message(cid, texts.share_geo_success, reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def text_content_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	# Обработка добавления аватарки
	if uid in READY_TO_REGISTER:
		if 'name' in READY_TO_REGISTER[uid]:
			if 'avatar' not in READY_TO_REGISTER[uid]:
				file_info = bot.get_file(message.photo[-1].file_id)
				downloaded_file = bot.download_file(file_info.file_path)
				photo_path = '{!s}{!s}.jpg'.format(config.AVARATRS_PATH, uid)
				with open(photo_path, 'wb') as new_file:
					new_file.write(downloaded_file)
				READY_TO_REGISTER[uid]['avatar'] = photo_path
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
				cm = database.get_communities()
				communities = [x['name'] for x in cm]
				for x in communities:
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
			# Проверка на ввод Имени и Фамилии
			if len(message.text.split(' ')) < 2:
				return bot.send_message(cid, texts.error_name_text)

			READY_TO_REGISTER[uid]['name'] = message.text

			# Попытка получения аватара пользователя
			user_avatars = bot.get_user_profile_photos(uid)
			if len(user_avatars.photos) > 0:
				avatar = user_avatars.photos[0][-1]
				file_info = bot.get_file(avatar.file_id)
				downloaded_file = bot.download_file(file_info.file_path)
				photo_path = '{!s}{!s}.jpg'.format(config.AVARATRS_PATH, uid)
				with open(photo_path, 'wb') as new_file:
					new_file.write(downloaded_file)
				READY_TO_REGISTER[uid]['avatar'] = photo_path
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
				cm = database.get_communities()
				communities = [x['name'] for x in cm]
				for x in communities:
					markup.add(x)
				markup.add('Другое')
				return bot.send_message(cid, texts.register_travel_type, reply_markup=markup)

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
			markup.row('Не сейчас')
			return bot.send_message(cid, texts.add_avatar_text, reply_markup=markup)
		elif 'avatar' not in READY_TO_REGISTER[uid]:
			if message.text == 'Не сейчас':
				READY_TO_REGISTER[uid]['avatar'] = 'default.jpg'
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
				cm = database.get_communities()
				communities = [x['name'] for x in cm]
				for x in communities:
					markup.add(x)
				markup.add('Другое')
				return bot.send_message(cid, texts.register_travel_type, reply_markup=markup)
			return bot.send_message(cid, texts.error_avatar_text)
		elif 'community' not in READY_TO_REGISTER[uid]:
			if message.text == 'Другое':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton('Узнать, кто такие сансерферы', url='http://sunsurfers.ru'))
				keyboard.add(types.InlineKeyboardButton('Узнать, кто такие сменщики', url='http://smenastation.com'))
				return bot.send_message(cid, texts.community_more_info_text, reply_markup=keyboard)

			cm = database.get_communities()
			communities = [x['name'] for x in cm]
			if message.text not in communities:
				return bot.send_message(cid, texts.error_button_text)
			READY_TO_REGISTER[uid]['community'] = message.text

			text = 'Ты выбрал сообщество {!s}'.format(READY_TO_REGISTER[uid]['community'])
			markup = types.ReplyKeyboardRemove()
			bot.send_message(cid, text, reply_markup=markup)

			for x in cm:
				if message.text == x['name']:
					READY_TO_REGISTER[uid]['community_id'] = x['id']

			# Проверка на присутсивие в white листе airtables
			if message.from_user.username:
				if database.is_user_in_whitelist('@{!s}'.format(message.from_user.username)):
					user = database.add_user(None, READY_TO_REGISTER[uid]['name'], READY_TO_REGISTER[uid]['avatar'],
						1, None, uid, None, READY_TO_REGISTER[uid]['community_id'])
					del READY_TO_REGISTER[uid]
					return bot.send_message(uid, texts.success_confirm_anket_text)

			# На данный момент нет пероприятияй для Смены, поэтому опускаем этот шаг
			if READY_TO_REGISTER[uid]['community'] == 'Станция Смена':
				READY_TO_REGISTER[uid]['events'] = ''
				READY_TO_REGISTER[uid]['events_text'] = ''
				return bot.send_message(cid, texts.register_confirm_people_text)
				'''
				READY_TO_REGISTER[uid]['confirm_people'] = ''

				user = database.add_user(None, READY_TO_REGISTER[uid]['name'], READY_TO_REGISTER[uid]['avatar'],
					0, None, uid, None, READY_TO_REGISTER[uid]['community_id'])

				# Отправить анкету в канал админов
				channel_text = 'Новая заявка №{!s}\n\n<a href="tg://user?id={!s}">Ссылка</a>\n\nИмя: {!s}\nСообщество: {!s}\nМероприятия: {!s}\nДоверенные люди: {!s}'.format(
					user['id'], uid, READY_TO_REGISTER[uid]['name'], READY_TO_REGISTER[uid]['community'], 
					READY_TO_REGISTER[uid]['events'], READY_TO_REGISTER[uid]['confirm_people'])
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirmanket_{!s}_{!s}'.format(user['id'], user['telegram'])))
				keyboard.add(types.InlineKeyboardButton('❌ Отклонить', callback_data='refuseanket_{!s}_{!s}'.format(user['id'], user['telegram'])))
				bot.send_photo(config.admin_channel_id, open(READY_TO_REGISTER[uid]['avatar'], 'rb'), 
					caption=channel_text, reply_markup=keyboard, parse_mode='HTML')

				logging.info('User {!s} anket sended to channel'.format(cid))

				del READY_TO_REGISTER[uid]
				markup = types.ReplyKeyboardRemove()
				return bot.send_message(cid, texts.register_complete, reply_markup=markup)
				'''

			READY_TO_REGISTER[uid]['event_ids'] = []
			READY_TO_REGISTER[uid]['events_text'] = ''
			typeofevents = database.get_all_typeofevents()
			keyboard = types.InlineKeyboardMarkup()
			for x in typeofevents:
				keyboard.add(types.InlineKeyboardButton(text=x['name'], callback_data='selecttypeofevent_{!s}'.format(x['id'])))
			return bot.send_message(cid, texts.register_type_events_question_text, reply_markup=keyboard)
		elif 'events' not in READY_TO_REGISTER[uid]:
			if len(READY_TO_REGISTER[uid]['event_ids']) == 0:
				text = 'Выбери хотя бы одно мероприятие'
				return bot.send_message(cid, text)

			READY_TO_REGISTER[uid]['events'] = message.text
			return bot.send_message(cid, texts.register_confirm_people_text)
		elif 'confirm_people' not in READY_TO_REGISTER[uid]:
			READY_TO_REGISTER[uid]['confirm_people'] = message.text

			user = database.add_user(None, READY_TO_REGISTER[uid]['name'], READY_TO_REGISTER[uid]['avatar'],
				0, None, uid, None, READY_TO_REGISTER[uid]['community_id'])

			if 'event_ids' in READY_TO_REGISTER[uid]:
				for x in READY_TO_REGISTER[uid]['event_ids']:
					database.add_user_event(user['id'], x)

			# Отправить анкету в канал админов
			channel_text = 'Новая заявка №{!s}\n\n<a href="tg://user?id={!s}">Ссылка</a>\n\nИмя: {!s}\nСообщество: {!s}\nМероприятия: {!s}\nДоверенные люди: {!s}'.format(
				user['id'], uid, READY_TO_REGISTER[uid]['name'], READY_TO_REGISTER[uid]['community'], 
				READY_TO_REGISTER[uid]['events_text'], READY_TO_REGISTER[uid]['confirm_people'])
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirmanket_{!s}_{!s}'.format(user['id'], user['telegram'])))
			keyboard.add(types.InlineKeyboardButton('❌ Отклонить', callback_data='refuseanket_{!s}_{!s}'.format(user['id'], user['telegram'])))
			bot.send_photo(config.admin_channel_id, open(READY_TO_REGISTER[uid]['avatar'], 'rb'), 
				caption=channel_text, reply_markup=keyboard, parse_mode='HTML')

			logging.info('User {!s} anket sended to channel'.format(cid))

			del READY_TO_REGISTER[uid]
			markup = types.ReplyKeyboardRemove()
			return bot.send_message(cid, texts.register_complete, reply_markup=markup)

	# Проверка на регистрацию прользователя
	user = database.get_user(uid)
	if not user:
		markup = types.ReplyKeyboardRemove()
		return bot.send_message(cid, texts.register_invite_text, reply_markup=markup)

	# Обработка отмены действий пользователя
	if message.text == '❌ Отменить':
		if uid in READY_TO_ADD_ABOUT:
			del READY_TO_ADD_ABOUT[uid]
		if uid in READY_TO_ADD_INSTA:
			del READY_TO_ADD_INSTA[uid]
		if uid in READY_TO_SHARE_LOCATION:
			del READY_TO_SHARE_LOCATION[uid]
		bot.send_message(cid, texts.cancel_text)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		for x in config.main_markup:
			markup.row(x)
		return bot.send_message(cid, texts.main_text, reply_markup=markup)

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
					bot.send_message(x['telegram'], READY_TO_ADMIN_EMAIL[uid]['text'])
				except Exception as e:
					print(e)
					continue

			del READY_TO_ADMIN_EMAIL[uid]
			bot.send_message(cid, texts.success_send_email_admin_text)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			for x in config.admin_markup:
				markup.add(x)
			return bot.send_message(cid, texts.admin_panel_greet_text, reply_markup=markup)

	# Обработка добавления about
	if uid in READY_TO_ADD_ABOUT:
		if 'text' not in READY_TO_ADD_ABOUT[uid]:
			# Ограничение на ввод не менее 10 и не более 30 слов
			if len(message.text.split(' ')) < 10 or len(message.text.split(' ')) > 30:
				text = 'Короткое описание себя должно быть не менее 10 и не более 30 слов.'
				return bot.send_message(cid, text)
			
			READY_TO_ADD_ABOUT[uid]['text'] = message.text

			# Обновить данные о пользователе в базе
			user = database.get_user(uid)
			database.update_user(user['id'], user['email'], user['name'], user['photo'], user['is_host'],
				READY_TO_ADD_ABOUT[uid]['text'], user['telegram'], user['insta'], user['community'])

			del READY_TO_ADD_ABOUT[uid]
			bot.send_message(cid, texts.about_updated)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			for x in config.setting_markup:
				markup.row(x)
			markup.row('↪️ В главное меню')
			return bot.send_message(cid, texts.settings_text, reply_markup=markup)

	# Обработка добавления insta
	if uid in READY_TO_ADD_INSTA:
		if 'text' not in READY_TO_ADD_INSTA[uid]:
			# Проверка валидности введенного юзернейм
			if not message.text.startswith('@'):
				text = 'Неверный формат!\n\nПример: @seva.randev'
				return bot.send_message(cid, text)

			# Преобразование в ссылку инстаграм
			READY_TO_ADD_INSTA[uid]['text'] = 'https://instagram.com/{!s}'.format(message.text[1:])

			# Обвновить данные о пользователе в базе
			user = database.get_user(uid)
			database.update_user(user['id'], user['email'], user['name'], user['photo'], user['is_host'],
				user['about'], user['telegram'], READY_TO_ADD_INSTA[uid]['text'], user['community'])

			del READY_TO_ADD_INSTA[uid]
			bot.send_message(cid, texts.insta_updated)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			for x in config.setting_markup:
				markup.row(x)
			markup.row('↪️ В главное меню')
			return bot.send_message(cid, texts.settings_text, reply_markup=markup)

	# Обработка отправки местоположения
	if uid in READY_TO_SHARE_LOCATION:
		return bot.send_message(cid, texts.share_geo_not_valid)

	# Обработка админ-панели
	if uid in config.ADMINS:
		if message.text == '📩 Создать рассылку':
			READY_TO_ADMIN_EMAIL[uid] = {}
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
			markup.add('❌ Отмена')
			return bot.send_message(cid, texts.ready_send_email_admin_text, reply_markup=markup)

	# Обработка основной клавиатуры пользователя
	if message.text == '📍 Поделиться геолокацией':
		READY_TO_SHARE_LOCATION[uid] = {}
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		markup.add(types.KeyboardButton(text="🗺 Отправить местоположение", request_location=True))
		markup.add('❌ Отменить')
		return bot.send_message(cid, texts.send_location_text, reply_markup=markup)
	elif message.text == '🗺 Посмотреть геолокации пользователей':
		user = database.get_user(uid)	
		token = str(uuid.uuid4()).replace('-', '')
		database.add_maplinks(user['id'], datetime.datetime.now(), 'all', token)

		maplink = '{!s}{!s}'.format(config.MAP_SERVER_DOMAIN, token)
		text = 'Карта доступна по ссылке в течение {!s} минут\n\n{!s}'.format(config.MAP_AVAILABLE_MINUTES, maplink)
		return bot.send_message(cid, text)
		'''
		communities = database.get_communities()

		keyboard = types.InlineKeyboardMarkup()
		for x in communities:
			keyboard.add(types.InlineKeyboardButton(x['name'], callback_data='showmapcommunity_{!s}'.format(x['id'])))
		keyboard.add(types.InlineKeyboardButton('Все пользователи', callback_data='showmapcommunity_all'))

		return bot.send_message(cid, texts.select_community_map, reply_markup=keyboard)
		'''
	elif message.text == '⚙️ Настройки':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		for x in config.setting_markup:
			markup.row(x)
		markup.row('↪️ В главное меню')
		return bot.send_message(cid, texts.settings_text, reply_markup=markup)

	# Возврат в главное меню
	if message.text == '↪️ В главное меню':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		for x in config.main_markup:
			markup.row(x)
		return bot.send_message(cid, texts.main_text, reply_markup=markup)

	# Обработка меню настроек
	if message.text == 'ℹ️ Рассказать о себе и своих интересах':
		READY_TO_ADD_ABOUT[uid] = {}
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		markup.row('❌ Отменить')
		about_text = ''
		user = database.get_user(uid)
		if user['about']:
			about_text = user['about']
		text = '{!s}\n\nВаши интересы на данный момент: {!s}'.format(texts.add_about, about_text)
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == '🎇 Дополнить мероприятия':
		typeofevents = database.get_all_typeofevents()
		keyboard = types.InlineKeyboardMarkup()
		for x in typeofevents:
			keyboard.add(types.InlineKeyboardButton(text=x['name'], callback_data='addselecttypeofevent_{!s}'.format(x['id'])))
		return bot.send_message(cid, texts.register_type_events_question_text, reply_markup=keyboard)
	elif message.text == '📱 Добавить ссылку на инстаграм':
		READY_TO_ADD_INSTA[uid] = {}
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
		markup.row('❌ Отменить')
		insta_text = ''
		user = database.get_user(uid)
		if user['insta']:
			insta_text = user['insta']
		text = '{!s}\nТвой инстаграм на данный момент: {!s}\n\nПример: @seva.randev'.format(texts.add_insta, insta_text)
		return bot.send_message(cid, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	cid = call.message.chat.id
	uid = call.from_user.id

	print(call.data)

	try:
		bot.answer_callback_query(call.id, '✅')
	except Exception as e:
		print(e)

	# Обработка подтверждения\отклонения новых анкет админом
	if call.data.startswith('confirmanket'):
		anket_id = int(call.data.split('_')[1])
		user_id = int(call.data.split('_')[2])
		database.confirm_user(anket_id)

		# Выслать уведомление пользователю
		try:
			bot.send_message(user_id, texts.success_confirm_anket_text)
		except Exception as e:
			print(e)

		return bot.edit_message_caption(texts.success_register, chat_id=cid, message_id=call.message.message_id)
	elif call.data.startswith('refuseanket'):
		anket_id = int(call.data.split('_')[1])
		user_id = int(call.data.split('_')[2])
		database.delete_all_user_events(anket_id)
		database.delete_user(anket_id)

		# Выслать уведомление пользователю
		try:
			bot.send_message(user_id, texts.unsuccess_confirm_anket_text)
		except Exception as e:
			print(e)

		return bot.edit_message_caption(texts.unsuccess_register, chat_id=cid, message_id=call.message.message_id)
	
	# Обработка выбора мероприятий при регистрации
	if call.data.startswith('selecttypeofevent'):
		typeofevent_id = int(call.data.split('_')[1])
		events = database.get_events_by_event_type_id(typeofevent_id)
		keyboard = types.InlineKeyboardMarkup()
		for x in events:
			month_name = util.get_month_name_by_number(x['date_of_the_event'].month)
			country = database.get_country_by_id(x['country'])
			event_name = '{!s}, {!s}, {!s} {!s}'.format(x['name'], country['name'], month_name, x['date_of_the_event'].year)
			keyboard.add(types.InlineKeyboardButton(text=event_name, callback_data='selectevent_{!s}'.format(x['id'])))
		keyboard.add(types.InlineKeyboardButton(text='↪️ Назад', callback_data='selectalltypeevents'))
		return bot.edit_message_text(texts.register_events_question_text, chat_id=cid, message_id=call.message.message_id, reply_markup=keyboard)
	elif call.data.startswith('selectevent'):
		event_id = int(call.data.split('_')[1])
		if uid not in READY_TO_REGISTER:
			text = 'Отправьте /start и повторите регистрацию'
			return bot.edit_message_text(text, chat_id=cid, message_id=call.message.message_id, reply_markup=None)
		event = database.get_event_by_id(event_id)
		text = 'Ты выбрал мероприятие {!s}'.format(event['name'])
		READY_TO_REGISTER[uid]['event_ids'].append(event_id)
		READY_TO_REGISTER[uid]['events_text'] += '{!s}\n'.format(event['name'])
		bot.edit_message_text(text, chat_id=cid, message_id=call.message.message_id, reply_markup=None)
		text = 'Желаешь отметить ещё мероприятия?'
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='➕ Добавить ещё', callback_data='selectalltypeevents'))
		keyboard.add(types.InlineKeyboardButton(text='➡️ Далее', callback_data='nextactionsafterevents'))
		return bot.send_message(cid, text, reply_markup=keyboard)
	elif call.data == 'selectalltypeevents':
		typeofevents = database.get_all_typeofevents()
		keyboard = types.InlineKeyboardMarkup()
		for x in typeofevents:
			keyboard.add(types.InlineKeyboardButton(text=x['name'], callback_data='selecttypeofevent_{!s}'.format(x['id'])))
		return bot.edit_message_text(texts.register_type_events_question_text, chat_id=cid, message_id=call.message.message_id, reply_markup=keyboard)
	elif call.data == 'nextactionsafterevents':
		if uid not in READY_TO_REGISTER:
			text = 'Отправьте /start и повторите регистрацию'
			return bot.edit_message_text(text, chat_id=cid, message_id=call.message.message_id, reply_markup=None)
		READY_TO_REGISTER[uid]['events'] = True
		return bot.send_message(cid, texts.register_confirm_people_text)

	# Обработка добавления новых мероприятий
	if call.data.startswith('addselecttypeofevent'):
		typeofevent_id = int(call.data.split('_')[1])
		events = database.get_events_by_event_type_id(typeofevent_id)
		user = database.get_user(uid)
		user_event_ids = [x['event'] for x in database.get_user_events(user['id'])]
		keyboard = types.InlineKeyboardMarkup()
		for x in events:
			if x['id'] in user_event_ids:
				continue
			month_name = util.get_month_name_by_number(x['date_of_the_event'].month)
			country = database.get_country_by_id(x['country'])
			event_name = '{!s}, {!s}, {!s} {!s}'.format(x['name'], country['name'], month_name, x['date_of_the_event'].year)
			keyboard.add(types.InlineKeyboardButton(text=event_name, callback_data='addselectevent_{!s}'.format(x['id'])))
		keyboard.add(types.InlineKeyboardButton(text='↪️ Назад', callback_data='addselectalltypeevents'))
		return bot.edit_message_text(texts.register_events_question_text, chat_id=cid, message_id=call.message.message_id, reply_markup=keyboard)
	elif call.data.startswith('addselectevent'):
		event_id = int(call.data.split('_')[1])
		event = database.get_event_by_id(event_id)
		text = 'Ты добавил мероприятие {!s}'.format(event['name'])
		user = database.get_user(uid)
		database.add_user_event(user['id'], event_id)
		bot.edit_message_text(text, chat_id=cid, message_id=call.message.message_id, reply_markup=None)
		text = 'Желаешь отметить ещё мероприятия?'
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='➕ Добавить ещё', callback_data='addselectalltypeevents'))
		return bot.send_message(cid, text, reply_markup=keyboard)
	elif call.data == 'addselectalltypeevents':
		typeofevents = database.get_all_typeofevents()
		keyboard = types.InlineKeyboardMarkup()
		for x in typeofevents:
			keyboard.add(types.InlineKeyboardButton(text=x['name'], callback_data='addselecttypeofevent_{!s}'.format(x['id'])))
		return bot.edit_message_text(texts.register_type_events_question_text, chat_id=cid, message_id=call.message.message_id, reply_markup=keyboard)
	'''
	elif call.data.startswith('showmapcommunity'):
		community_id = call.data.split('_')[1]

		user = database.get_user(uid)		
		token = str(uuid.uuid4()).replace('-', '')
		database.add_maplinks(user['id'], datetime.datetime.now(), community_id, token)

		maplink = '{!s}{!s}'.format(config.MAP_SERVER_DOMEN, token)
		text = 'Карта доступна по ссылке в течение {!s} минут\n\n{!s}'.format(config.MAP_AVAILABLE_MINUTES, maplink)
		return bot.edit_message_text(text, chat_id=cid, message_id=call.message.message_id)
	'''


if __name__ == '__main__':
	main(bot)
