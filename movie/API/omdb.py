import requests

class OMDBAPI():
    # def getDataByDataID(self, dataId):
    #     imdbId = Link.objects.get(dataId__exact=dataId)
    #     if len(imdbId) < 7:
    #         imdbId = 'tt0' + imdbId
    #     else:
    #         imdbId = 'tt' + imdbId
    #     url = self.url + 'i=' + imdbId
    #     info = requests.get(url).json()
    #     moviename = info['Title']
    #     movieyear = info['Year']
    #     runtime = info['Runtime']
    #     poster = info['Poster']
    #     imdbRating = info['imdbRating']
    #     imdbId = info['imdbId']
    #     plot = info['Plot']
    #
    #     return Movie.objects.create(moviename, movieyear, runtime, poster, imdbRating, imdbId, plot)

    def getDataByImdbID(imdbId):
        url = 'http://www.omdbapi.com/?' + 'i=' + imdbId
        info = requests.get(url).json()

        movieInfo = {
            'moviename': info['Title'],
            'movieyear': info['Year'],
            'runtime': info['Runtime'],
            'poster': info['Poster'],
            'imdbRating': info['imdbRating'],
            'imdbId': info['imdbID'],
            'plot': info['Plot']
        }

        return movieInfo