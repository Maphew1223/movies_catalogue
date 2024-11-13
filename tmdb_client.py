import requests

def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOTY0ZjViYzRmNjBjZjY0NjNkOGE0MTdhNTVhMTA0ZiIsIm5iZiI6MTczMTUwMDI1My43MjM5MDEzLCJzdWIiOiI2NzM0OTU4NTljMWEyMzhkOGE5ZDQyMDciLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.isfdTuIjrT6A5JThEzfmiWvW124p5JThIfwWVeZQzeI"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many):
    data = get_popular_movies()
    return data["results"][:how_many]