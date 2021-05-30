import pymongo
from decouple import config
from pymongo import MongoClient


client = pymongo.MongoClient(config('MONGO_URI'))
Database = client.get_database('botmovies')
print("database connected!")
db = Database.movies


def on_start(user_id):
	newUser = {
		"user_id": user_id,
        "movies": [],
        "watched": [],
    }
	db.insert_one(newUser)


def get_not_user(user_id):	
	data = db.find_one({"user_id": user_id})
	if data == None:
		return True
	else: 
		return False


def get_list(user_id):	
	data = db.find_one({"user_id": user_id})
	return data['movies']


def get_watched_list(user_id):	
	data = db.find_one({"user_id": user_id})
	return data['watched']


def insert_movie(data,user_id):
	movie_data = get_list(user_id)
	movie_data.append(data)	
	db.find_one_and_update({"user_id": user_id},{ '$set': { "movies" : movie_data} })	


def rm_movie(data,user_id):
	if data > 0:
		movie_data = get_list(user_id)
		movie_data.pop(data-1)	
		db.find_one_and_update({"user_id": user_id},{ '$set': { "movies" : movie_data} })
		return True
	else:
		return False


def watched_movie(data,user_id):
	if data > 0:
		movie_data = get_list(user_id)
		watched_data = get_watched_list(user_id)
		watched_data.append(movie_data[(data-1)])
		movie_data.pop(data-1)
		db.find_one_and_update({"user_id": user_id},{ '$set': { "movies" : movie_data, "watched": watched_data } })
		return True
	else:
		return False
