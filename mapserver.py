#!/usr/bin/env python3

import json
import datetime

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
				map_description = 'Имя: {!s}<br>О себе: {!s}<br>Инстаграм: {!s}'.format(user['name'], user['about'], user['insta'])
				last_visited_places_filtered[str(user['id'])]['map_description'] = map_description
	last_visited_places = last_visited_places_filtered

	# Сгенерировать geojson feature для вывода на карту
	geojson_feature = []
	for x in last_visited_places:
		geojson_feature.append({
			'type': 'Feature',
			'properties': {
				'description': last_visited_places[x]['map_description'],
				'icon': 'rocket'
			},
			'geometry': {
				'type': 'Point',
				'coordinates': [last_visited_places[x]['coordinates'].split(' ')[0], last_visited_places[x]['coordinates'].split(' ')[1]]
			}
		})

	geojson_feature = {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": geojson_feature
        }
    }
	print(geojson_feature)

	return render_template('map.html', geojson_feature=json.dumps(geojson_feature))


if __name__ == '__main__':
	app.run(host=config.MAP_SERVER_HOST, port=config.MAP_SERVER_PORT, debug=config.DEBUG)
