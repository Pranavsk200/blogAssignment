from django.shortcuts import render,redirect
import requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login,logout
from .models import Blog

API_KEY = 'a43e59eae98b44e592a26f1d64bc11c2'


def home(request):
    if request.user.is_authenticated:
        country = 'in'

        if country:
            url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
            response = requests.get(url)
            data = response.json()
            articles = data['articles']
        else:
            url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
            response = requests.get(url)
            data = response.json()
            articles = data['articles']

        context = {
            'articles' : articles
        }

        return render(request, 'news_api/home.html', context)
    else:
        return redirect("login")    

def signin(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['pass']
        repassword = request.POST['repass']
        if password==repassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"user name already exists,please resistor with another username") 
                return redirect("signin")   
            else:    
                user =User.objects.create_user(username=username, password=password)
                user.save()
                print('user created')
                return redirect("login")
        else:
            messages.info(request, "conform passowerd and password are not matching")
    else:
        return render(request, "news_api/signin.html") 

def login(request):
    if request.method=='POST':
        name = request.POST['username']
        password = request.POST['pass']
        user=authenticate(request, username=name, password=password)
        if user is not None:
            dj_login(request, user)
            current_user=request.user
            return redirect("home")
        else:
            #messages.success(request, "username or password is incorrect") 
            return redirect("login")   
    else:    
        return render(request,"news_api/login.html")         

def logoutUser(request):
    if request.user.is_authenticated: 
        logout(request)
        return redirect("login") 
    else:
        return redirect("login")
    
def blog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            user = request.user
            saveBlog = Blog(title=title,content=content,author=user)
            saveBlog.save()
            messages.info(request,"Your blog is posted")
            return redirect("blogs") 

        blogs = Blog.objects.all()
        context={
            'blogs':blogs
        }    
        return render(request, 'news_api/blogs.html', context)
    else:
        return redirect("login")    

def myblog(request):
    if request.user.is_authenticated:
        user = request.user
        blogs = Blog.objects.filter(author = user)
        context={
            "myblogs":blogs
        }
        return render(request, "news_api/myblogs.html", context)
    else:
        return redirect("login")    

def editBlog(request, id=None):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']
            blog = blog = Blog.objects.filter(id=id)[0]
            blog.title = title
            blog.content = content
            blog.save()
            messages.info(request, "Your blog is updated")
            return redirect("myblogs")
        blog = Blog.objects.filter(id=id)[0]
        if blog.author.username == request.user.username:
            context={
                'i':blog
            }
            return render(request, 'news_api/editBlog.html', context)
        else:
            return redirect("myblogs") 
    else:
        return redirect("login")          

def deleteBlog(request, id=id):
    if request.user.is_authenticated:
        blog = Blog.objects.filter(id=id)[0]
        if blog.author.username == request.user.username:
            blog.delete()
            messages.info(request, "Your blog is deleted")
            return redirect("myblogs")
    else:
        return redirect("login")        

