import pandas as pd
from .data_manager_interface import DataManagerInterface


def read_csv_file(filename):
    df = pd.read_csv(filename)
    data = {'data': []}

    for _, row in df.iterrows():
        person = next((item for item in data['data'] if item['id'] == row['id']), None)
        if person is None:
            person = {'id': int(row['id']), 'name': row['name'], 'movies': []}
            data['data'].append(person)

        movie_columns = [col for col in row.index if col.startswith('movies_')]
        for column in movie_columns:
            if pd.notnull(row[column]):
                movie_index = int(column.split('_')[1])
                movie_id = int(row[f'movies_{movie_index}_id'])
                if not any(movie['id'] == movie_id for movie in person['movies']):
                    movie = {
                        'id': int(row[f'movies_{movie_index}_id']),
                        'name': row[f'movies_{movie_index}_name'],
                        'director': row[f'movies_{movie_index}_director'],
                        'year': int(row[f'movies_{movie_index}_year']),
                        'rating': float(row[f'movies_{movie_index}_rating'])
                    }
                    person['movies'].append(movie)

    return data


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        data = read_csv_file(self.filename)
        return_list = [{'id': item['id'], 'name': item['name']} for item in data['data']]
        return return_list

    def get_user_movies(self, user_id):
        data = read_csv_file(self.filename)
        return_list = []
        for user in data['data']:
            if user['id'] == user_id:
                return_list = [
                    {
                        'id': movie['id'],
                        'name': movie['name'],
                        'director': movie['director'],
                        'year': movie['year'],
                        'rating': movie['rating']
                    } for movie in user['movies']]
        return return_list
