from telegram.ext import *
from decouple import config
import random
import db
import os

print("Bot started....")


def start_command(update,context):
	if db.get_not_user(update['message']['chat']['id']):		
		db.on_start(update['message']['chat']['id'])
		update.message.reply_text("Welcome "+ update['message']['chat']['first_name'])
	else:
		update.message.reply_text("Welcome back "+ update['message']['chat']['first_name'])


def help_command(update,context):
	helptxt=f"""
	    Hi {update['message']['chat']['first_name']}!
		
    	/add <New movie name> Add a movie to your watchlist
    	/list List of movies to watch
	    /random Pick a random number of movies from the watchlist
    	/watched <Index number of movie> Tell naive_movies_bot you've watched this movie (and remove it from your watchlist)
	    /finished List of movies you have finished
    	/remove <Index number of movie> Remove a movie from your watchlist

		 
	"""
	update.message.reply_text(helptxt)


def add_command(update,context):
	args = context.args
	user_id = update['message']['chat']['id']
	global data
	data = ""
	for arg in args:
		data = data + arg + " "
	if data != "":
		db.insert_movie(data,user_id)
		update.message.reply_text("\"" + data + "\" added to list")
	else:
		update.message.reply_text("One argument is required!")


def rm_command(update,context):
	user_id = update['message']['chat']['id']
	args = context.args
	if len(args)>1:
		update.message.reply_text("Only one argument is allowed!")
	elif len(args)==0:
		update.message.reply_text("One argument is required!")
	else:
		data = int(args[0])						
		if db.rm_movie(data,user_id):
			update.message.reply_text("remove successfull")
		else:
			update.message.reply_text("U might have entered a non-existing movie number")


def list_command(update,context):	
	update.message.reply_text("Your movies to watch =>")
	user_id = update['message']['chat']['id']
	data = db.get_list(user_id)
	if len(data) != 0:
		global listMovies
		listMovies = ""
		for i in range(len(data)):
			listMovies = listMovies + str(i+1) + ": " + data[i] +"\n"	
		update.message.reply_text(listMovies)
	else:
		update.message.reply_text("You don't have any movies. Use /add <movie name> to add new movies.")


def watched_command(update,context):
	user_id = update['message']['chat']['id']
	args = context.args
	if len(args)>1:
		update.message.reply_text("Only one argument is allowed!")
	elif len(args)==0:
		update.message.reply_text("One argument is required!")
	else:
		data = int(args[0])						
		if db.watched_movie(data,user_id):
			update.message.reply_text("added to finished")
		else:
			update.message.reply_text("U might have entered a non-existing movie number")


def random_command(update,context):
	user_id = update['message']['chat']['id']
	data = db.get_list(user_id)
	if len(data) != 0:
		randomMovie = random.choices(data, k = 1)
		update.message.reply_text(randomMovie[0])
	else:
		update.message.reply_text("You don't have any movies. Use /add <movie name> to add new movies.")


def finished_command(update,context):
	update.message.reply_text("You finished watching =>")	
	user_id = update['message']['chat']['id']
	data = db.get_watched_list(user_id)
	if len(data) != 0:
		global listWMovies
		listWMovies = ""
		for i in range(len(data)):
			listWMovies = listWMovies + str(i+1) + ": " + data[i] +"\n"	
		update.message.reply_text(listWMovies)
	else:
		update.message.reply_text("You don't have any movies in the finished list. Use /watched <movie number> to add movie to finished list.")	


def handle_msg(update,context):
	user_msg = str(update.message.text).lower()	
	update.message.reply_text(user_msg)


def error(update,context):
	print(f"Update {update} caused error {context.error}")
	update.message.reply_text("There is an error. Pls report it via naiverecomm@gmail.com")


def main():
	PORT = int(os.environ.get('PORT', '8443'))
	updater = Updater(config('API_KEY'),use_context=True)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start",start_command))
	dp.add_handler(CommandHandler("help",help_command,pass_args=True))
	dp.add_handler(CommandHandler("add",add_command,pass_args=True))
	dp.add_handler(CommandHandler("remove",rm_command,pass_args=True))
	dp.add_handler(CommandHandler("list",list_command))
	dp.add_handler(CommandHandler("random",random_command))
	dp.add_handler(CommandHandler("watched",watched_command,pass_args=True))
	dp.add_handler(CommandHandler("finished",finished_command))
	#dp.add_handler(MessageHandler(Filters.text, handle_msg))	
	dp.add_error_handler(error)

	updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=config('API_KEY'),
                          webhook_url='https://naive-movies-bot.herokuapp.com/' + config('API_KEY'))
	updater.idle()

main()