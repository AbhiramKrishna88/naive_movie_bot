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


varss = ["sopranos","madmen","Malcolm & Marie Zendaya","what woman want","irakal 1985","Marley & Me","after we collided","malcolm and marie","The Rider 2017- Chloe Zhao","Then you came(2018)","Girl from nowhere series","the serpent 1Q","line of duty 5Q","oththa seruppu size 7 R9.5","pennyworth","kumatti 1979 YT","riders of justice 2020","its okay not to be okay kdrama","3665 repeat the year kdrama","vincenzo kdrama","The Gangster, The Cop, The Devil","Ballon 2018","shot caller 2017","biriyani","coming to America 1988","the waterboy 1998","I, robot 2004","moneyball","eight men out -sports -black sox scandal","mouse kdrama","The odd family:Zombie on sale","Sense 8","see 2019 Aquaman Apple 8 episodes","elite netflix","mitchells vs machines","Series Pennyworth Gotham THe orginals,tvd, twd,lost better call saul marvel series see,sense 8,banshee,fargo","cinema paradiso","miracle in room no:7","visaarnai","crime of the century hbo max doc","mad max fury road","The Killing 2011","westworld","Looking for alaska","doom patrol🌟","ubelievable mini series","before we go","The night of","upiter's legacy","halston 2021","trying bbc","the underground railroad","Death and Nightingales novel eugene","too close","veneno hbo max","kingdom 12eps netflix","This Is the End 2013","Gangs of London 9 episodes","'Behind her eyes' 6ep 5hr KL","Calls 9 eps 2022","reply 1988 romantic doctor itaewon class sweet home who are you","but if u want to watch some.. i'll recommend the gifted series nd bad genius the series THAI kesh"] 