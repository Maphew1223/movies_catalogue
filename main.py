from flask import Flask, render_template, request
import tmdb_client

app = Flask(__name__)

@app.route('/')
def homepage():
    list_types = {
        'top_rated': 'Top rated',
        'upcoming': 'Upcoming',
        'popular': 'Popular',
        'now_playing': 'Now Playing'
    }
    selected_list_type = request.args.get('list_type', 'popular')
    if selected_list_type not in list_types:
        selected_list_type = 'popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list_type)
    return render_template("homepage.html", movies=movies, list_types=list_types, selected_list_type=selected_list_type)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}



@app.route("/movie/<movie_id>")
def movie_details(movie_id):
   details = tmdb_client.get_single_movie(movie_id)
   cast = tmdb_client.get_single_movie_cast(movie_id)
   return render_template("movie_details.html", movie=details, cast=cast)

if __name__ == '__main__':
    app.run(debug=True)