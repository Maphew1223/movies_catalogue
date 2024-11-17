import pytest
from unittest.mock import Mock
import requests
from main import app


from tmdb_client import (
    get_popular_movies,
    get_movies_list,
    get_poster_url,
    get_movies,
    get_single_movie,
    get_single_movie_cast
)

API_TOKEN = "dummy_api_token"

@pytest.fixture
def mock_requests_get(monkeypatch):
    mock_get = Mock()
    monkeypatch.setattr(requests, "get", mock_get)
    return mock_get

@pytest.fixture
def mock_api_token(monkeypatch):
    monkeypatch.setattr("tmdb_client.API_TOKEN", API_TOKEN)

def test_get_popular_movies(mock_requests_get, mock_api_token):
    fake_response = {"results": [{"id": 1, "title": "Popular Movie"}]}
    mock_requests_get.return_value.json.return_value = fake_response

    movies = get_popular_movies("popular")

    assert movies["results"][0]["title"] == "Popular Movie"
    mock_requests_get.assert_called_once_with(
        "https://api.themoviedb.org/3/movie/popular",
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )

def test_get_movies_list(mock_requests_get, mock_api_token):
    fake_response = {"results": [{"id": 1, "title": "Movie"}]}
    mock_requests_get.return_value.json.return_value = fake_response

    movies = get_movies_list("top_rated")

    assert movies["results"][0]["title"] == "Movie"
    mock_requests_get.assert_called_once_with(
        "https://api.themoviedb.org/3/movie/top_rated",
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )

def test_get_poster_url():
    poster_path = "poster.jpg"
    url = get_poster_url(poster_path, size="w500")
    assert url == "https://image.tmdb.org/t/p/w500/poster.jpg"

def test_get_movies(mock_requests_get, mock_api_token):
    fake_response = {"results": [{"id": 1, "title": "Movie 1"}, {"id": 2, "title": "Movie 2"}]}
    mock_requests_get.return_value.json.return_value = fake_response

    movies = get_movies("popular", how_many=1)

    assert len(movies) == 1
    assert movies[0]["title"] == "Movie 1"

def test_get_single_movie(mock_requests_get, mock_api_token):
    fake_response = {"id": 1, "title": "Single Movie"}
    mock_requests_get.return_value.json.return_value = fake_response

    movie = get_single_movie(1)

    assert movie["title"] == "Single Movie"
    mock_requests_get.assert_called_once_with(
        "https://api.themoviedb.org/3/movie/1",
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )

def test_get_single_movie_cast(mock_requests_get, mock_api_token):
    fake_response = {"cast": [{"id": 1, "name": "Actor 1"}, {"id": 2, "name": "Actor 2"}]}
    mock_requests_get.return_value.json.return_value = fake_response

    cast = get_single_movie_cast(1)

    assert len(cast) == 2
    assert cast[0]["name"] == "Actor 1"
    mock_requests_get.assert_called_once_with(
        "https://api.themoviedb.org/3/movie/1/credits",
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )

@pytest.mark.parametrize("list_type", ["popular", "top_rated", "now_playing", "upcoming"])
def test_homepage(monkeypatch, list_type):
    expected_movies = [
        {"id": i, "title": f"{list_type.title()} Movie {i}"}
        for i in range(1, 3)
    ]
    
    api_mock = Mock(return_value=expected_movies)
    monkeypatch.setattr("tmdb_client.get_movies", api_mock)

    with app.test_client() as client:
        response = client.get(f"/?list_type={list_type}")

        assert response.status_code == 200
        api_mock.assert_called_once_with(how_many=8, list_type=list_type)

