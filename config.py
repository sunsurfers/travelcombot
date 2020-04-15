import os
from enum import Enum

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEBUG = False
PROXY = {'https': os.getenv('PROXY_STRING')}
LOGGER_PATH = 'logging.log'
AVARATRS_PATH = 'avatars/'

# ID Telegram админов в боте
# @fomchenkov_v: 217166737
# @nemelnikov: 263156959
# @skywinder = 84380711
ADMINS = [217166737, 263156959, 84380711]

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

if DEBUG:
    MAP_SERVER_DOMAIN = 'http://0.0.0.0:8080/'
else:
    MAP_SERVER_DOMAIN = 'http://5.187.5.95:8080/'

# Время доступности ссылки на карту в минутах
MAP_AVAILABLE_MINUTES = 10


class MainMarkup(Enum):
    share_loc = '📍 Поделиться геолокацией'
    show_loc = '🗺 Посмотреть геолокации пользователей'
    goto_settings = '⚙️ Настройки'


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
