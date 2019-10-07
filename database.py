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
			sql = 'INSERT INTO users (email, name, photo, is_host, about, telegram, insta, community) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(sql, (email, name, photo, is_host, about, telegram, insta, community))
			connection.commit()
			sql = 'SELECT * FROM users WHERE id = LAST_INSERT_ID()'
			cursor.execute(sql)
		return cursor.fetchone()
	finally:
		connection.close()


def get_all_users():
	"""
	Получить всех пользователей бота
	"""
	connection = get_connection()
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM users'
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
			sql = 'SELECT * FROM users WHERE telegram=%s'
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
			sql = 'UPDATE users SET is_host=1 WHERE id=%s'
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
			sql = 'DELETE FROM users WHERE id=%s'
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
			sql = 'SELECT * FROM communities'
			cursor.execute(sql)
			return cursor.fetchall()
		connection.commit()
	finally:
		connection.close()
