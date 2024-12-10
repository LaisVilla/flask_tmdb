import requests
from models.movie import Movie
from config import Config

class TMDBService:
    @staticmethod
    def get_popular_movies(page=1):
        url = f"{Config.TMDB_BASE_URL}/movie/popular"
        params = {
            'api_key': Config.TMDB_API_KEY,
            'page': page,
            'language': 'pt-BR'
        }
        response = requests.get(url, params=params)
        if response.ok:
            movies = response.json()['results']
            return [Movie(movie_data) for movie_data in movies]
        return []

    @staticmethod
    def get_movie_details(movie_id):
        url = f"{Config.TMDB_BASE_URL}/movie/{movie_id}"
        params = {
            'api_key': Config.TMDB_API_KEY,
            'language': 'pt-BR',
            'append_to_response':'credits,watch/providers'  # Adicionando credits à requisição
        }
        response = requests.get(url, params=params)
        if response.ok:
            return Movie(response.json())
        return None
 
    @staticmethod
    def get_movie_videos(movie_id):
        url = f"{Config.TMDB_BASE_URL}/movie/{movie_id}/videos"
        params = {
            'api_key': Config.TMDB_API_KEY,
            'language': 'pt-BR'
        }
        response = requests.get(url, params=params)
        if response.ok:
            videos = response.json().get('results', [])
            # Filter for YouTube trailers, preferably official ones
            trailers = [
                video for video in videos 
                if video['site'] == 'YouTube' and 
                video['type'] in ['Trailer', 'Teaser'] and
                'official' in video['name'].lower()
            ]
            # If no official trailers found, get any YouTube trailer
            if not trailers:
                trailers = [
                    video for video in videos 
                    if video['site'] == 'YouTube' and 
                    video['type'] in ['Trailer', 'Teaser']
                ]
            return trailers[0] if trailers else None
        return None

    @staticmethod
    def search_movies(query, page=1):
        url = f"{Config.TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': Config.TMDB_API_KEY,
            'query': query,
            'page': page,
            'language': 'pt-BR'
        }
        response = requests.get(url, params=params)
        if response.ok:
            movies = response.json()['results']
            return [Movie(movie_data) for movie_data in movies]
        return []
