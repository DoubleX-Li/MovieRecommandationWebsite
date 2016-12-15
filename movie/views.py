import random

from django import forms
from django.http import HttpResponse
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
    return render(request, 'movie/regist.html', {'form': form, 'isLogin': True})


# 登陆
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('uname:' + username)
        # form = UserForm(request.POST)
        # if form.is_valid():
        #     username = form['username'].value()
        #     password = form['password'].value()
        #     user = User.objects.filter(username__exact=username, password__exact=password)
        #     if user:
        #         # 比较成功，跳转index
        #         response = HttpResponseRedirect('/movie/index/')
        #         # 将username写入浏览器cookie,失效时间为3600
        #         response.set_cookie('username', username, 3600)
        #         response.set_cookie('userid', user[0].id, 3600)
        #         return response
        #     else:
        #         # 比较失败，还在login
        #         return HttpResponseRedirect('/movie/login/')
        user = User.objects.filter(username__exact=username, password__exact=password)
        if user:
            # 比较成功
            response = render(request, 'movie/index.html', context={'username': username, 'isLogin': True})
            response.set_cookie('username', username, 3600)
            return response
        else:
            return render(request, 'movie/index.html', {'isLogin': False})
    return render(request, 'movie/index.html', {'isLogin': False})


# 登陆成功
def index(req):
    username = req.COOKIES.get('username', '')
    return render(req, 'movie/index.html', {'username': username, 'isLogin': True})


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
        userid = 1
        rating_list = Rating.objects.all().filter(userId__exact=userid)
        movie_list = []
        for rating in rating_list:
            imdbid = calImdbId(Link.objects.get(dataId__exact=rating.dataId).movieId)
            movie_list.append((Movie.objects.get(imdbId__exact=imdbid), rating.rating))
        return movie_list

    def get_context_data(self, **kwargs):
        context = super(WatchedView, self).get_context_data(**kwargs)
        context['isLogin'] = True
        context['username'] = self.request.COOKIES.get('username')
        return context


class DetailView(generic.DetailView):
    model = Movie
    template_name = 'movie/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['isLogin'] = True
        context['username'] = self.request.COOKIES.get('username')
        return context


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
        for recommand in recommandMovies:
            recommand_list.append((Movie.objects.filter(imdbId=recommand.imdbId)[0], round(recommand.rating / 2, 2)))
        if len(recommandMovies) >= num:
            print("无需查询")
        else:
            still_need_num = num - len(recommandMovies)
            print("Still need num:" + str(still_need_num))
            still_need_name_list = RecommandAPI().getRecommand(still_need_num)
            for still_need_name in still_need_name_list:
                recommand_list.append((Movie.getByImdbId(still_need_name.imdbId), still_need_name.rating))
        print("最终列表长：" + str(len(recommand_list)))
        return recommand_list

    def get_context_data(self, **kwargs):
        context = super(RecommandView, self).get_context_data(**kwargs)
        context['isLogin'] = True
        context['username'] = self.request.COOKIES.get('username')
        return context


def browse(request):
    username = request.COOKIES.get('username', '')
    userid = request.COOKIES.get('userid', '')
    num = 6
    movie_list = Movie.objects.all()
    movie_sum = len(movie_list)
    random_index_list = []
    random_movie_list = []
    while len(random_index_list) < num:
        random_index = random.randint(1, movie_sum) - 1
        if random_index in random_index_list:
            pass
        else:
            random_index_list.append(random_index)
            random_movie_list.append(movie_list[random_index])
    return render(request, 'movie/browse.html',
                  {'username': username, 'userid': userid, 'random_movie_list': random_movie_list, 'isLogin': True})


# 退出
def logout(request):
    response = render(request, 'movie/index.html', {'isLogin': False})
    # 清理cookie里保存username
    response.delete_cookie('username')
    return response
