import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
DEBUG = False
PROXY = {'https': os.getenv('PROXY_STRING')}
LOGGER_PATH = 'logging.log'
AVARATRS_PATH = 'avatars/'
# ID Telegram админов в боте
ADMINS = [217166737, 263156959]

# MySQL данные для авторизации
db_host = 'mysql'
db_user = 'root'
db_password = ''
db_database = ''
db_charset = 'utf8'

# ID Telegram канала для подтверждение анкет пользователей
admin_channel_id = -1001346987455

# Данные локального сервера карты
MAP_SERVER_HOST = '0.0.0.0'
MAP_SERVER_PORT = 8080
MAP_SERVER_DOMEN = 'http://0.0.0.0:8080/'

if not DEBUG:
    MAP_SERVER_DOMEN = 'http://5.187.5.95:8080/'

# Время доступности ссылки на карту в минутах
MAP_AVAILABLE_MINUTES = 10

main_markup = [
    '📍 Поделиться геолокацией',
    '🗺 Посмотреть геолокации пользователей',
    '⚙️ Настройки',
]

setting_markup = [
    'ℹ️ Рассказать о себе и своих интересах',
    '🎇 Дополнить мероприятия',
    '📱 Добавить ссылку на инстаграм',
]

admin_markup = [
    '📩 Создать рассылку',
]

try:
    from local_config import *
except ImportError:
    pass
