from django.shortcuts import render
from django.core.paginator import Paginator
import os
import json
import sqlite3


class Movie:
    def __init__(self, title=None, description=None, img_url=None, genre=None, runtime=None, imdb_url=None, rating=None, metascore=None):
        self.title = title if title else None
        self.img = img_url if img_url else None
        self.runtime = runtime if runtime else None
        self.genre = genre if genre else None
        self.imdb = imdb_url if imdb_url else "web/static/images/stock.jpeg"
        self.description = description if description else None
        self.rating = rating if rating else None
        self.metascore = metascore if metascore else None


def getMovies(id_list=[]):

    conn = sqlite3.connect(os.path.join(os.getcwd(), 'Data', 'Movie.db'))
    c = conn.cursor()
    Movies = []
    exists = {}
    for movie_id in id_list:
        try:
            _ = exists[movie_id]
        except KeyError:
            exists[movie_id] = None
            c.execute(""" SELECT title, description, img_url, genre, runtime, imdb_url, rating, metascore FROM Movie WHERE id = :id """, {
                      'id': movie_id})
            movie = c.fetchone()
            Movies.append(
                Movie(title=movie[0], description=movie[1], img_url=movie[2], genre=', '.join(eval(movie[3])), runtime=movie[4], imdb_url=movie[5], rating=movie[6], metascore=movie[7]))
    conn.close()
    return Movies


def home(request):
    q = request.GET.get('q')
    result_list_id = []
    if q:
        f = open(os.path.join(os.getcwd(), 'Data', 'index.json'))

        data = json.load(f)
        for word in q.lower().split(' '):
            try:
                sub_dict = data[str(word)]

                for year in sorted(sub_dict.keys(), reverse=True):
                    result_list_id.extend(sub_dict[year])
            except KeyError:
                pass
    movies = getMovies(id_list=result_list_id)
    length = len(movies)
    data = Paginator(movies, 18)
    page = request.GET.get('page')
    page_obj = data.get_page(page)

    context = {
        'page_obj': page_obj,
        'length': length,
        'movies': movies,
    }
    template = 'web/home.html'
    return render(request, template, context)


def results(request):
    context = {}
    template = 'web/results.html'
    return render(request, template, context)
