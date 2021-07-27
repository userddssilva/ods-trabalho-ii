import json
import platform
from .connection import Connection

connection = Connection()

if platform.system() == 'Linux':
    FILE_PATH = open('/home/indtusuario/github/ods-trabalho-ii/app/backend/animes.json')
else:
    FILE_PATH = open('C:\\Users\\Douglas\\Desktop\\ods-trabalho-ii\\app\\backend\\animes.json')
animes_json = json.load(FILE_PATH)


def manhattan(rating1, rating2):
    distance = 0
    total = 0
    for key in rating1:
        if key in rating2 and key != "name":
            distance += abs(rating1[key] - rating2[key])
            total += 1
    return distance


def computeNearestNeighbor(input_anime_id):
    animes_json = connection.get_all_animes_json()
    animes_json = json.loads(animes_json)
    input_anime = animes_json[input_anime_id]
    distances = []
    for anime_id, anime in animes_json.items():
        if anime != input_anime:
            distance = manhattan(anime, input_anime)
            distances.append((distance, anime_id))
    distances.sort()
    return distances[:20]
