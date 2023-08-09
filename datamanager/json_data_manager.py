import json
import requests
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.api_key = '3c3d7378'

    def open_file(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
            return data

    def save_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_username(self, user_id):
        data = self.open_file()
        user_list = [{'id': item['id'], 'name': item['name'], 'bio': item['bio']} for item in data['data']]
        for item in user_list:
            if item['id'] == user_id:
                return item['name']

    def get_all_users(self):
        data = self.open_file()
        return_list = [{'id': item['id'], 'name': item['name'], 'bio': item['bio']} for item in data['data']]
        return return_list

    def get_user_movies(self, user_id):
        data = self.open_file()
        return_list = []
        for user in data['data']:
            if user['id'] == user_id:
                return_list = [
                    {
                        'id': movie['id'],
                        'name': movie['name'],
                        'year': movie['year'],
                        'director': movie['director'],
                        'plot': movie['plot'],
                        'rating': movie['rating'],
                        'poster': movie['poster']
                    } for movie in user['movies']]
        return return_list

    def add_user(self, username, userbio):
        data = self.open_file()

        if data['data']:
            max_id = [max(id['id'] for id in data['data'])]
           
            user_id = max_id[0] + 1
        else:
            user_id = 1

        movies = []
        new_user_dict = {'id': user_id, 'name': username, 'bio': userbio, 'movies': movies}
        data['data'].append(new_user_dict)

       
        self.save_data(data)

    def add_movie(self, user_id, moviename):
        url = f'http://www.omdbapi.com/?apikey={self.api_key}&t={moviename}'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                movie_data = response.json()

                if movie_data['Response'] == 'True':
                    data = self.open_file()
                    if self.get_user_movies(user_id):
                        max_id = max(movie['id'] for user in data['data'] for movie in user['movies'])
                        movie_id = max_id + 1
                    else:
                        movie_id = 1

                    movie_title = movie_data['Title']
                    movie_year = movie_data['Year']
                    movie_director = movie_data['Director']
                    movie_plot = movie_data['Plot']
                    movie_poster = movie_data['Poster']
                    movie_rating = movie_data['imdbRating']

                    new_movie_dict = {
                        'id': movie_id,
                        'name': movie_title,
                        'director': movie_director,
                        'year': movie_year,
                        'plot': movie_plot,
                        'rating': movie_rating,
                        'poster': movie_poster
                    }

                    data['data'][user_id - 1]['movies'].append(new_movie_dict)
                    self.save_data(data)
                else:
                    error_message = movie_data['Error']
                    print(f'Movie data not found: {error_message}')
            else:
                print('Error occurred during API request')
        except requests.exceptions.RequestException as e:
            print(f'Request Exception: {e}')

    def delete_user(self, user_id):
        data = self.open_file()
        users = data['data']

        for user in users:
            if user['id'] == user_id:
                users.remove(user)
                self.save_data(data)
                return

    def delete_movie(self, user_id, movie_id):
        data = self.open_file()
        for user in data['data']:
            if user['id'] == user_id:
                movies = user['movies']
                for movie in movies:
                    if movie['id'] == movie_id:
                        movies.remove(movie)
                        break
                break
        self.save_data(data)

    def get_user(self, user_id):
        data = self.open_file()
        users = data['data']

        for user in users:
            if user['id'] == user_id:
                return user

    def save_user(self, user):
        data = self.open_file()
        for item in data['data']:
            if item['id'] == user['id']:
                item['name'] = user['name']
                item['bio'] = user['bio']
                break
        self.save_data(data)
