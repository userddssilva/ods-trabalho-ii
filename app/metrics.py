from backend import connection

connection = connection.Connection()

users = connection.getUsers()
users = [x for x,_,_ in users]

for user in users:
	animes_user = connection.get_animes_user(user)
	recomends = connection.get_recommendations(user)
	recomends = [y for _,y,_ in recomends]
	tp = 0
	fp = 0
	for anime_id, rate in animes_user:
		if anime_id in recomends:
			if rate >= 3:
				tp += 1
			else:
				fp += 1
	print(F"user_id={user}, Pression = {tp/(tp+fp)}")
	# print(animes_user)
	# print(recomends)

# print(users)