import requests

from movie.models import Movie, Recommand


def parseMoviename(moviename):
    if moviename.__contains__('"'):
        moviename = moviename[1:]
    return moviename


class RecommandAPI():
    def getRecommand(self, num):
        url = 'http://192.168.1.105:8888/0/ratings/top/' + str(num)
        r = requests.get(url).json()
        movies = []
        # 解析返回的list
        for movie in r:
            moviename = parseMoviename(movie[0])
            movierating = movie[1]
            ratingnum = movie[2]
            imdbid = Movie.getByMovieName(moviename).imdbId
            recommand = Recommand.objects.create(userId=1, imdbId=imdbid, rating=movierating)
            movies.append(recommand)
        return movies
