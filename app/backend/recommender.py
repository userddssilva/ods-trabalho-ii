import itertools
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


def computeNearestNeighbor(rated_animes):
    neighbors = []
    animes_json = connection.get_all_animes_json()
    animes_json = json.loads(animes_json)

    max_interations = 5
    while len(neighbors) <= 100 and max_interations >= 0:
        for rated_anime in rated_animes:
            input_anime = animes_json[rated_anime]
            distances = []
            for anime_id, anime in animes_json.items():
                if anime_id not in rated_animes:
                    if anime != input_anime:
                        distance = manhattan(anime, input_anime)
                        neighbor = (distance, anime_id)
                        distances.append(neighbor)
            for d in distances[:40]:
                if d[1] not in neighbors:
                    neighbors.append(d[1])
            print(f"##=Computing neighbors = {len(neighbors)}")
            print(f"##=Iterations = {max_interations}")
            if  len(neighbors) >= 100 and max_interations >=0:
                break
        max_interations -= 1
    return neighbors
