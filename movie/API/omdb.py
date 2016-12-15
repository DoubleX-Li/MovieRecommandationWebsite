import requests


class OMDBAPI():
    def getDataByImdbID(imdbId):
        url = 'http://www.omdbapi.com/?' + 'i=' + imdbId
        proxy = {'localhost': 1920}
        info = requests.get(url, proxies=proxy).json()

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
