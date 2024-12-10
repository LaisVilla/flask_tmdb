# controllers/movie_controller.py
from flask import Blueprint, render_template, request
from services.tmdb_service import TMDBService

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    movies = TMDBService.get_popular_movies(page=page)
    return render_template('index.html', movies=movies, current_page=page)

@movies_bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = TMDBService.get_movie_details(movie_id)
    if not movie:
        return render_template('404.html'), 404
    
    # Get trailer data
    video_data = TMDBService.get_movie_videos(movie_id)
    if video_data:
        movie.load_video_data(video_data)
        
    return render_template('movie_details.html', movie=movie)

@movies_bp.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    if query:
        movies = TMDBService.search_movies(query, page=page)
    else:
        movies = []
    return render_template('search.html', movies=movies, query=query, current_page=page)