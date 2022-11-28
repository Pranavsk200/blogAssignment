from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("signin",views.signin, name="signin"),
    path("login",views.login, name="login"),
    path("logout",views.logoutUser, name="logout"),
    path("blogs",views.blog, name="blogs"),
    path("myblogs",views.myblog, name="myblogs"),
    path("editBlogs/<int:id>",views.editBlog, name="editBlogs"),
    path("deleteBlogs/<int:id>",views.deleteBlog, name="deleteBlogs")
]
