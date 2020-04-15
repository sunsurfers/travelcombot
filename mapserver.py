#!/usr/bin/env python3

import json
import datetime

import geohash
from flask import Flask
from flask import render_template

import database
import config


app = Flask(__name__)


@app.route('/<token>', methods=['GET'])
def map_router(token):
	maplink = database.get_maplink_by_token(token)

	# Проверка на существование токена
	if not maplink:
		return render_template('fail.html')

	# Проверка на истечение времени доступности карты
	if maplink['createdate'] + datetime.timedelta(minutes=config.MAP_AVAILABLE_MINUTES) < datetime.datetime.now():
		database.delete_maplink(maplink['id'])
		return render_template('fail.html')

	users = database.get_all_users()
	visited_places = database.get_all_visited_places()

	# Получить последнее посещенное место для каждого пользователя бота
	last_visited_places = {} # user_id: data
	for x in visited_places:
		last_visited_places[str(x['user'])] = x

	# Фильтрация карты по выбранным сообществам путещественников
	last_visited_places_filtered = {}
	for user in users:
		if maplink['community'] == 'all' or str(user['community']) == str(maplink['community']):
			if str(user['id']) in last_visited_places:
				last_visited_places_filtered[str(user['id'])] = last_visited_places[str(user['id'])]
				last_visited_places_filtered[str(user['id'])]['community'] = user['community']

				if not user['about']:
					user['about'] = 'Не указано'
				if not user['insta']:
					user['insta'] = 'Не указано'

				map_description = 'Имя: {!s}<br>О себе: {!s}<br>Инстаграм: <a target="_blank" href="{!s}">{!s}</a>'.format(
					user['name'], user['about'], user['insta'],  user['insta']
				)
				map_description += '<br>Написать в телеграм: <a target="_blank" href="tg://user?id={!s}">открыть</a>'.format(
					user['telegram']
				)
				map_description += '<br>Дата обновления локации: {!s}'.format(
					str(last_visited_places_filtered[str(user['id'])]['date']).split(' ')[0]
				)

				last_visited_places_filtered[str(user['id'])]['map_description'] = map_description
	last_visited_places = last_visited_places_filtered

	# Сгенерировать geojson feature для вывода на карту
	geojson_feature = []
	for x in last_visited_places:
		geohash_code = geohash.encode(
			float(last_visited_places[x]['coordinates'].split(' ')[0]),
			float(last_visited_places[x]['coordinates'].split(' ')[1]), 
			precision = 5,  # Коэффициент неточности местоположения
		)
		coords = geohash.decode(geohash_code)

		json_data = {
			'type': 'Feature',
			'properties': {
				'description': last_visited_places[x]['map_description'],
				# 'icon': 'rocket'
			},
			'geometry': {
				'type': 'Point',
				'coordinates': [coords[0], coords[1]]
			}
		}

		# Вывести иконку в соответствии с сообщестом
		if int(last_visited_places[x]['community']) == 1:
			json_data['properties']['icon'] = 'bar'
		else:
			json_data['properties']['icon'] = 'rocket'

		geojson_feature.append(json_data)

	geojson_feature = {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': geojson_feature
        }
    }
	print(geojson_feature)

	return render_template('map.html', geojson_feature=json.dumps(geojson_feature))


if __name__ == '__main__':
	app.run(host=config.MAP_SERVER_HOST, port=config.MAP_SERVER_PORT, debug=config.DEBUG)
