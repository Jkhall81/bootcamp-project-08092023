from datamanager.data_manager_interface import DataManagerInterface
from flask import session
from models import User, Movie, db
import json
import requests

class SQLiteDataManager(DataManagerInterface):
	def __init__(self, db_file_name):
		self.db = db
		self.api_key = '3c3d7378'

	def get_all_users(self):
		users = User.query.all()
		return users

	def get_user_movies(self, user_id):
		movies = Movie.query.filter_by(user_id=user_id).all()
		return movies

	def add_user(self, name, email, password, bio):
		new_user = User(name=name, email=email, password=password, bio=bio)
		db.session.add(new_user)
		db.session.commit()
		

	def add_movie(self, user_id, moviename):
		url = f'http://www.omdbapi.com/?apikey={self.api_key}&t={moviename}'

		try:
				response = requests.get(url)

				if response.status_code == 200:
					movie_data = response.json()

					if movie_data['Response'] == 'True':
						
						movie_title = movie_data['Title']
						movie_year = movie_data['Year']
						movie_director = movie_data['Director']
						movie_plot = movie_data['Plot']
						movie_poster = movie_data['Poster']
						movie_rating = movie_data['imdbRating']
						user_id = user_id

						new_movie = Movie(name=movie_title, director=movie_director, year=movie_year, plot=movie_plot, rating=movie_rating, poster=movie_poster, user_id=user_id)
						db.session.add(new_movie)
						db.session.commit()
						return 200

					else:
						error_message = movie_data['Error']
						print(f'Movie data not found: {error_message}')

				else:
					print('Error occurred during API request!')

		except requests.exceptions.RequestException as e:
			print(f'Request Exception: {e}')

	def update_movie(self):
		pass

	def delete_movie(self, user_id, movie_id):
		movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
		db.session.delete(movie)
		db.session.commit()

	def get_user(self, user_id):
		user = User.query.get(user_id)
		return user
