from flask import Blueprint, jsonify, request
from forms.forms import csrf
from models import Movie
from datamanager.sqlite_data_manager import SQLiteDataManager

api_bp = Blueprint('api', __name__)
data_manager = SQLiteDataManager('data/db.sqlite3')


@api_bp.route('/users', methods=['GET'])
def get_users():
	data = []
	users = data_manager.get_all_users()
	for user in users:
		data.append({
			'id': user.id,
			'name': user.name,
			'email': user.email,
			'bio': user.bio
		})
		
	return jsonify(data)


@csrf.exempt
@api_bp.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def get_users_movies(user_id):
	"""
	{
		"moviename": "name_of_movie"
	}

	this must be in the body of the post request, for it to work.
	"""
	if request.method == 'POST':

		data = request.get_json()
		movie_name = data.get('moviename')
		

		api_call = data_manager.add_movie(user_id, movie_name)

		new_movie = Movie.query.filter(Movie.name == movie_name).first()
		if api_call == 200:
			return jsonify({"message": "Movie successfully added!"})

		else:
			return jsonify({"message": "Movie not found, try again!  Make sure the body of your post request contains {\"moviename\": \"name_of_movie\"}"})

	movies = data_manager.get_user_movies(user_id)
	data = []
	for movie in movies:
		data.append({
			'id': movie.id,
			'name': movie.name,
			'director': movie.director,
			'year': movie.year,
			'plot': movie.plot,
			'rating': movie.rating,
			'poster': movie.poster
		})
	
	return jsonify(data)
