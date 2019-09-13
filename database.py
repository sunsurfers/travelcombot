import pymysql.cursors

import config


def create_tables():
	"""
	Создать необходимые таблицы в базе данных
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
			# Пользователи бота
			sql = '''
			CREATE TABLE IF NOT EXISTS `users` (
				`id` int(11) NOT NULL AUTO_INCREMENT,
				`uid` varchar(255) UNIQUE COLLATE utf8_general_ci NOT NULL,
				`register_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
				`name` varchar(255) COLLATE utf8_general_ci NOT NULL,
				`avatar_path` varchar(255) COLLATE utf8_general_ci NOT NULL,
				`community` varchar(255) COLLATE utf8_general_ci NOT NULL,
				`last_events` varchar(255) COLLATE utf8_general_ci,
				`confirm_people` varchar(255) COLLATE utf8_general_ci,
				`social_links` varchar(255) COLLATE utf8_general_ci,
				`is_confirm` int(1),
				PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
			AUTO_INCREMENT=1;
			'''
			cursor.execute(sql)
		connection.commit()
	finally:
		connection.close()


def add_user(uid, register_date, name, avatar_path, community, 
		last_events, confirm_people, social_links, is_confirm):
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
			sql = 'INSERT INTO users (uid, register_date, name, avatar_path, community, last_events, confirm_people, social_links, is_confirm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(sql, (uid, register_date, name, avatar_path, community, last_events, confirm_people, social_links, is_confirm))
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
			sql = 'SELECT * FROM users'
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
			sql = 'SELECT * FROM users WHERE uid=%s'
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
			sql = 'UPDATE users SET is_confirm=1 WHERE id=%s'
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
			sql = 'DELETE FROM users WHERE id=%s'
			cursor.execute(sql, (id,))
		connection.commit()
	finally:
		connection.close()
