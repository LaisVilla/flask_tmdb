# app.py
from flask import Flask
from controllers.movie_controller import movies_bp

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(movies_bp)

if __name__ == '__main__':
    app.run(debug=True)