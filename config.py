import os


BOT_TOKEN = os.environ['BOT_TOKEN']
DEBUG = True  # TODO
PROXY = {'https': os.environ['PROXY_STRING']}
LOGGER_PATH = 'logging.log'
AVARATRS_PATH = 'avatars/'

# MySQL данные для авторизации
# CREATE DATABASE `travelcombot` CHARACTER SET utf8 COLLATE utf8_general_ci;
db_host = 'localhost'
db_user='root'
db_password='123456'
db_database='travelcombot'
db_charset = 'utf8'

# ID Telegram канала для подтверждение анкет полльзователей
admin_channel_id = -1001346987455

community_types = [
	'Сансерферы',
	'Смена',
]
