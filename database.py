import pymysql.cursors

import config


def add_user(email, name, photo, is_host, about, telegram, insta, community):
	"""
	Добавить заявку пользователя в базу данных
	"""
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = 'INSERT INTO users (email, name, photo, is_host, about, telegram, insta, community) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(sql, (email, name, photo, is_host, about, telegram, insta, community))
			connection.commit()
			sql = 'SELECT * FROM users ORDER BY id DESC LIMIT 1'
			cursor.execute(sql)
		return cursor.fetchone()
	finally:
		connection.close()


def get_all_users():
	"""
	Получить всех пользователей бота
	"""
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
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
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
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
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
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
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
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
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM community'
			cursor.execute(sql)
			return cursor.fetchall()
		connection.commit()
	finally:
		connection.close()
