# models/movie.py
class Movie:
    def __init__(self, data):
        self.video_data = None
        self.id = data.get('id')
        self.title = data.get('title')
        self.overview = data.get('overview')
        self.poster_path = data.get('poster_path')
        self.release_date = data.get('release_date')
        self.vote_average = data.get('vote_average')
        self.backdrop_path = data.get('backdrop_path')
        self.genres = data.get('genres', [])
        # Modificação na inicialização do elenco
        credits = data.get('credits', {})
        if isinstance(credits, dict):
            self.cast = credits.get('cast', [])
        else:
            self.cast = []
            
        self.streaming_providers = data.get('watch/providers', {}).get('results', {}).get('BR', {})
        

    def load_video_data(self, video_data):
        self.video_data = video_data

    @property
    def trailer_url(self):
        if self.video_data and self.video_data.get('key'):
            return f"https://www.youtube.com/embed/{self.video_data['key']}"
        return None
    
    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

    @property
    def backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None

    @property
    def main_cast(self):
        return self.cast[:10] if self.cast else []

    @property
    def available_platforms(self):
        if not self.streaming_providers:
            return {}
        return {
            'flatrate': self.streaming_providers.get('flatrate', []),
            'rent': self.streaming_providers.get('rent', []),
            'buy': self.streaming_providers.get('buy', [])
        }