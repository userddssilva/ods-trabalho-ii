import json
import platform

if platform.system() == 'Linux':
    FILE_PATH = open('/home/indtusuario/github/ods-trabalho-ii/app/backend/animes.json')
else:
    FILE_PATH = open('C:\\Users\\Douglas\\Desktop\\ods-trabalho-ii\\app\\backend\\animes.json')
animes_json = json.load(FILE_PATH)


def manhattan(rating1, rating2):
    distance = 0
    total = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            total += 1
    return distance


def computeNearestNeighbor(input_anime):
    distances = []
    for anime in animes_json:
        if anime != input_anime:
            distance = manhattan(animes_json[anime], animes_json[input_anime])
            distances.append((distance, anime))
    distances.sort()
    map_anime = list(map(lambda x: {"anime": x[1], "distance": x[0]}, distances))
    return json.dumps(map_anime[:10])