import random

from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from movie.API.recommand import RecommandAPI
from movie.models import User, Movie, Link, Recommand, Rating


# 表单
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=100)
    password = forms.CharField(label="密码", widget=forms.PasswordInput())


# 注册
def regist(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = User.objects.create(username=username, password=password)
            return HttpResponse('注册成功！' + user.__str__())

    form = UserForm()
    return render(request, 'movie/regist.html', {'form': form})


# 登陆
def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/movie/index/')
                # 将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', username, 3600)
                response.set_cookie('userid', user[0].id, 3600)
                return response
            else:
                # 比较失败，还在login
                return HttpResponseRedirect('/movie/login/')
    form = UserForm()
    return render(request, 'movie/login.html', {'form': form})


# 登陆成功
def index(req):
    username = req.COOKIES.get('username', '')
    print("Username::" + username)

    return render(req, 'movie/index.html', {'username': username})

# 根据link表单中的不完整imdbid计算真正的imdbid
def calImdbId(imdbId):
    num = 7 - len(str(imdbId))
    result = 'tt'
    for i in range(num):
        result += '0'
    result += str(imdbId)
    return result

class WatchedView(generic.ListView):
    template_name = 'movie/watched.html'
    context_object_name = 'watched_list'

    def get_queryset(self):
        """
        :return:当前用户看过的电影list
        """
        userid = self.request.GET.get('userid')
        userid = 1
        rating_list = Rating.objects.all().filter(userId__exact=userid)
        movie_list = []
        for rating in rating_list:
            imdbid = calImdbId(Link.objects.get(dataId__exact=rating.dataId).movieId)
            movie_list.append(Movie.objects.get(imdbId__exact=imdbid))
        return movie_list

class DetailView(generic.DetailView):
    model = Movie
    template_name = 'movie/detail.html'

# def watched(request):
#     username = request.COOKIES.get('username', '')
#     watchedList = User.objects.get(username__exact=username).getWatched()
#     watchedListDetail = []
#     errorMessage = ''
#     for watchedMovie in watchedList:
#         dataId = Link.objects.get(dataId__exact=watchedMovie.dataId).dataId
#         movie = Movie.getByDataId(dataId=dataId)
#         if movie:
#             watchedListDetail.append(movie)
#         else:
#             errorMessage += "没有找到电影" + dataId
#     return render(request, 'movie/watched.html',
#                   {'username': username, 'watchedListDetail': watchedListDetail, 'errorMessage': errorMessage})

class RecommandView(generic.ListView):
    template_name = 'movie/recommand.html'
    context_object_name = 'recommand_list'

    def get_queryset(self):
        """
        :return:返回推荐的电影列表
        """
        userid = 1
        num = 50
        recommand_list = []
        recommandMovies = Recommand.objects.all().filter(userId__exact=userid)
        print("库中有的推荐信息有：" + str(len(recommandMovies)))
        if len(recommandMovies) >= num:
            print("无需查询")
            print(recommandMovies)
            recommand_list = Movie.objects.all().filter(imdbId__in=recommandMovies)
        else:
            recommand_list += Movie.objects.all().filter(imdbId__in=recommandMovies)
            still_need_num = num - len(recommandMovies)
            print("Still need num:" + str(still_need_num))
            still_need_name_list = RecommandAPI().getRecommand(still_need_num)
            for still_need_name in still_need_name_list:
                recommand_list.append(Movie.getByImdbId(still_need_name.imdbId))
        print("最终列表长：" + str(len(recommand_list)))
        return recommand_list

# def recommand(request):
#     username = request.COOKIES.get('username', '')
#     userid = request.COOKIES.get('userid', '')
#     num = 50
#     recommandMoviesDetail = []
#     errorMessage = ''
#     recommandMovies = Recommand.objects.all().filter(userId__exact=userid)
#     if len(recommandMovies) == 0:
#         print("推荐信息未找到，获取")
#         recommandMovies = RecommandAPI().getRecommand(num)
#         for recommandMovie in recommandMovies:
#             movie = Movie.getByMovieName(recommandMovie[0])
#             if movie:
#                 print("得到了：" + movie.moviename)
#                 Recommand.objects.create(userId=userid, imdbId=movie.imdbId)
#                 recommandMoviesDetail.append(movie)
#             else:
#                 errorMessage += "没有找到电影" + recommandMovie[0]
#     else:
#         print("推荐信息找到，从数据库中读取")
#         for recommandMovie in recommandMovies:
#             movie = Movie.getByImdbId(recommandMovie.imdbId)
#             if movie:
#                 print("得到了：" + movie.moviename)
#                 recommandMoviesDetail.append(movie)
#             else:
#                 errorMessage += "没有找到电影" + recommandMovie[0]
#     return render(request, 'movie/recommand.html',
#                   {'username': username, 'recommandMoviesDetail': recommandMoviesDetail, 'errorMessage': errorMessage})

def browse(request):
    username = request.COOKIES.get('username', '')
    userid = request.COOKIES.get('userid', '')
    movies = Movie.objects.all()
    movienum = len(movies)
    randomnum = random.randint(1, movienum)
    movie = movies[randomnum]
    return render(request, 'movie/browse.html', {'username': username, 'userid': userid, 'movie': movie})


# 退出
def logout(req):
    response = HttpResponse('logout !!')
    # 清理cookie里保存username
    response.delete_cookie('username')
    return response
