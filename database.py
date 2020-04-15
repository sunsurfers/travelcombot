import pymysql.cursors

import config


def get_connection():
	return pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)


def add_user(email, name, photo, is_host, about, telegram, insta, community):
	"""
	Добавить заявку пользователя в базу данных
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'INSERT INTO user (email, name, photo, is_host, about, telegram, insta, community) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(sql, (email, name, photo, is_host, about, telegram, insta, community))
			connection.commit()
			sql = 'SELECT * FROM user WHERE id = LAST_INSERT_ID()'
			cursor.execute(sql)
		return cursor.fetchone()
	finally:
		connection.close()


def update_user(id, email, name, photo, is_host, about, telegram, insta, community):
	"""
	Обновить пользователя
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'UPDATE user SET email=%s, name=%s, photo=%s, is_host=%s, about=%s, telegram=%s, insta=%s, community=%s WHERE id=%s'
			cursor.execute(sql, (email, name, photo, is_host, about, telegram, insta, community, id))
		connection.commit()	
	finally:
		connection.close()


def get_all_users():
	"""
	Получить всех пользователей бота
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM user'
			cursor.execute(sql)
		return cursor.fetchall()
	finally:
		connection.close()


def get_user(uid):
	"""
	Получить заявку пользователя
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM user WHERE telegram=%s'
			cursor.execute(sql, (uid,))
		return cursor.fetchone()
	finally:
		connection.close()


def confirm_user(id):
	"""
	Подтвердить заявку
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'UPDATE user SET is_host=1 WHERE id=%s'
			cursor.execute(sql, (id,))
		connection.commit()
	finally:
		connection.close()


def delete_user(id):
	"""
	Удалить заявку пользователя
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'DELETE FROM user WHERE id=%s'
			cursor.execute(sql, (id,))
		connection.commit()
	finally:
		connection.close()


def get_communities():
	"""
	Получить все сообщества
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM community'
			cursor.execute(sql)
			return cursor.fetchall()
	finally:
		connection.close()


def get_all_typeofevents():
	"""
	Получить все доступные типо событий
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM typeofevent'
			cursor.execute(sql)
			return cursor.fetchall()
	finally:
		connection.close()


def get_events_by_event_type_id(typeofevent_id):
	"""
	Получить мероприятия по ID типа мероприятия
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM event WHERE type_of_event=%s'
			cursor.execute(sql, (typeofevent_id,))
			return cursor.fetchall()
	finally:
		connection.close()


def get_event_by_id(event_id):
	"""
	Получить мероприятие по ID
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM event WHERE id=%s'
			cursor.execute(sql, (event_id,))
			return cursor.fetchone()
	finally:
		connection.close()


def add_user_event(user_id, event_id):
	"""
	Добавить мероприятие пользователя
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'INSERT INTO event_user (event, user) VALUES (%s, %s)'
			cursor.execute(sql, (event_id, user_id))
		connection.commit()
	finally:
		connection.close()


def delete_all_user_events(id):
	"""
	Удалить все мероприятия пользователя
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'DELETE FROM event_user WHERE user=%s'
			cursor.execute(sql, (id,))
		connection.commit()
	finally:
		connection.close()


def get_user_events(user_id):
	"""
	Получить мероприятия пользователя
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM event_user WHERE user=%s'
			cursor.execute(sql, (user_id,))
		return cursor.fetchall()
	finally:
		connection.close()


def is_user_in_whitelist(username):
	"""
	Проверка на присутствие пользователя в white листе
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM whitelist WHERE username=%s'
			cursor.execute(sql, (username,))
		return cursor.fetchone()
	finally:
		connection.close()


def add_user_to_white_list(name, username, phone=None):
	"""
	Добавить пользователя в white лист
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'INSERT INTO whitelist (name, username, phone) VALUES (%s, %s, %s)'
			cursor.execute(sql, (name, username, phone))
		connection.commit()
	finally:
		connection.close()


def get_country_by_id(country_id):
	"""
	Получить страну по ID
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM country WHERE id=%s'
			cursor.execute(sql, (country_id,))
		return cursor.fetchone()
	finally:
		connection.close()


def add_visited_place(user, coordinates, city, date):
	"""
	Добавить посещенное место
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'INSERT INTO visited_paces (user, coordinates, city, date) VALUES (%s ,%s, %s, %s)'
			cursor.execute(sql, (user, coordinates, city, date))
		connection.commit()
	finally:
		connection.close()


def get_all_visited_places():
	"""
	Получить всем посещенные места
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM visited_paces'
			cursor.execute(sql)
		return cursor.fetchall()
	finally:
		connection.close()


def add_maplinks(user, createdate, community, token):
	"""
	Добавить новую ссылку на карту
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'INSERT INTO maplinks (user, createdate, community, token) VALUES (%s ,%s, %s, %s)'
			cursor.execute(sql, (user, createdate, community, token))
		connection.commit()
	finally:
		connection.close()


def get_maplink_by_token(token):
	"""
	Получить ссылку на карту по токену
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM maplinks WHERE token=%s'
			cursor.execute(sql, (token,))
			return cursor.fetchone()
	finally:
		connection.close()


def delete_maplink(id):
	"""
	Удалить ссылку на карту
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'DELETE FROM maplinks WHERE id=%s'
			cursor.execute(sql, (id,))
		connection.commit()
	finally:
		connection.close()
