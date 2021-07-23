import json

f = open('animes_json.json')
animes_json = json.load(f)

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
    return distances[:10]

def recommend(input_anime, animes):
    nearest = computeNearestNeighbor(input_anime, animes)[0][1]

    recommendations = []
    neighborRatings = animes[nearest]
    animeRatings = animes[input_anime]
    for artist in neighborRatings:
        if not artist in animeRatings:
            recommendations.append((artist, neighborRatings[artist]))
    return sorted(recommendations, key=lambda artistTuple: artitTuple[1], reverse = True)

print(computeNearestNeighbor("Kimi no Na wa."))
