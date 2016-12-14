from django.db import models

from movie.API.omdb import OMDBAPI


def calImdbId(imdbId):
    num = 7 - len(str(imdbId))
    result = 'tt'
    for i in range(num):
        result += '0'
    result += str(imdbId)
    return result

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def getWatched(self):
        userid = User.objects.get(username__exact=self.username).id
        wathcedList = Rating.objects.all().filter(userId=userid)
        return wathcedList

class Movie(models.Model):
    moviename = models.CharField(max_length=50, verbose_name='电影名称')
    movieyear = models.IntegerField(verbose_name='发行年份')
    runtime = models.CharField(max_length=50, verbose_name='时长')
    poster = models.CharField(max_length=500, verbose_name='封面链接')
    imdbRating = models.FloatField(verbose_name='IMDB评分')
    imdbId = models.CharField(max_length=50, verbose_name='IMDBID')
    plot = models.CharField(max_length=500, verbose_name='简要情节', default='...')

    def __str__(self):
        return self.moviename

    def getByDataId(dataId):
        imdbId = Link.objects.get(dataId__exact=dataId).movieId
        imdbId = calImdbId(imdbId)
        movie = Movie.objects.all().filter(imdbId__exact=imdbId)
        if len(movie) == 0:
            print("在OMDB查询")
            info = OMDBAPI.getDataByImdbID(imdbId)
            movie = Movie.objects.create(moviename=info['moviename'],
                                         movieyear=info['movieyear'],
                                         runtime=info['runtime'],
                                         poster=info['poster'],
                                         imdbRating=info['imdbRating'],
                                         imdbId=info['imdbId'],
                                         plot=info['plot'])
            return movie
        else:
            print("在数据库中找到")
            return movie[0]

    def getByMovieName(moviename):
        data = Data.objects.all().filter(dataname__contains=moviename)[0]
        dataid = data.id
        movie = Movie.getByDataId(dataid)
        return movie

class Data(models.Model):
    dataname = models.CharField(max_length=50, verbose_name='数据名称')

class Rating(models.Model):
    userId = models.IntegerField()
    dataId = models.IntegerField()
    rating = models.FloatField(default=0, verbose_name='评分')

class Link(models.Model):
    dataId = models.IntegerField()
    movieId = models.IntegerField()

