import requests

def get_popular_movies(list_type):
    endpoint = {
        "popular": "https://api.themoviedb.org/3/movie/popular",
        "top_rated": "https://api.themoviedb.org/3/movie/top_rated",
        "upcoming": "https://api.themoviedb.org/3/movie/upcoming",
        "now_playing": "https://api.themoviedb.org/3/movie/now_playing"
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint[list_type], headers=headers)
    return response.json()

def get_movies_list(list_type):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(list_type, how_many):
    data = get_popular_movies(list_type)
    return data["results"][:how_many]

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOTY0ZjViYzRmNjBjZjY0NjNkOGE0MTdhNTVhMTA0ZiIsIm5iZiI6MTczMTUwMDI1My43MjM5MDEzLCJzdWIiOiI2NzM0OTU4NTljMWEyMzhkOGE5ZDQyMDciLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.isfdTuIjrT6A5JThEzfmiWvW124p5JThIfwWVeZQzeI"

def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()["cast"]

