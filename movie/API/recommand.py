import requests

def parseMoviename(moviename):
    if moviename.__contains__('"'):
        moviename = moviename[1:]
    # if moviename.__contains__(' ('):
    #     index = moviename.index(' (')
    #     moviename = moviename[:index]
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
            movies.append([moviename, movierating, ratingnum])
        return movies