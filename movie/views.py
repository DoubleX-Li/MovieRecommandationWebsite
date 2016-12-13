from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from movie.models import User, Rating, Movie, Link


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

    return render(req, 'movie/index.html')

def watched(request):
    username = request.COOKIES.get('username', '')
    watchedList = User.objects.get(username__exact=username).getWatched()
    watchedListDetail = []
    errorMessage = ''
    for watchedMovie in watchedList:
        dataId = Link.objects.get(dataId__exact=watchedMovie.dataId).dataId
        movie = Movie.getByDataId(dataId=dataId)[0]
        if movie:
            watchedListDetail.append(movie)
        else:
            errorMessage += "没有找到电影" + dataId
    print("查看详情")
    for i in watchedListDetail:
        print(i.moviename)
    return render(request, 'movie/watched.html', {'username': username,'watchedListDetail':watchedListDetail, 'errorMessage':errorMessage})

# 退出
def logout(req):
    response = HttpResponse('logout !!')
    # 清理cookie里保存username
    response.delete_cookie('username')
    return response