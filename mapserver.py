#!/usr/bin/env python3

import json

from flask import Flask
from flask import render_template

import database
import config


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
	users = database.get_all_users()
	visited_places = database.get_all_visited_places()

	# Получить последнее мосещенное место для каждого пользователя бота
	last_visited_places = {} # user_id: data
	for x in visited_places:
		last_visited_places[str(x['user'])] = x

	# Сгенерировать geojson feature для вывода на карту
	geojson_feature = []
	for x in last_visited_places:
		geojson_feature.append({
			'type': 'Feature',
			'properties': {
				'description': 'Описание',  # TODO
				'icon': 'rocket'
			},
			'geometry': {
				'type': 'Point',
				'coordinates': [last_visited_places[x]['coordinates'].split(' ')[0], last_visited_places[x]['coordinates'].split(' ')[1]]
			}
		})

	geojson_feature = json.dumps({
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": geojson_feature
        }
    })
	print(geojson_feature)

	return render_template('map.html', geojson_feature=geojson_feature)


if __name__ == '__main__':
	app.run(host=config.MAP_SERVER_HOST, port=config.MAP_SERVER_PORT, debug=config.DEBUG)
