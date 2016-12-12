from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Movie(models.Model):
    moviename = models.CharField(max_length=50, verbose_name='电影名称')
    movieyear = models.IntegerField(verbose_name='发行年份')
    runtime = models.IntegerField(verbose_name='时长')
    poster = models.CharField(max_length=500, verbose_name='封面链接')
    imdbRating = models.FloatField(verbose_name='IMDB评分')
    imdbId = models.CharField(max_length=50, verbose_name='IMDBID')

    def __str__(self):
        return self.moviename

class Data(models.Model):
    dataname = models.CharField(max_length=50, verbose_name='数据名称')

class Rating(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.FloatField(default=0, verbose_name='评分')

class Links(models.Model):
    dataId = models.IntegerField()
    movieId = models.IntegerField()

