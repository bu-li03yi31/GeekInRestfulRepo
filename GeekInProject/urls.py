"""GeekInProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from GeekInRest import views
from GeekInRest import userViews

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', views.login),
    url(r'^createUser/', userViews.createUser),
    url(r'^newPost/', views.createNewPost),
    url(r'^addLike/', views.addLike),
    url(r'^removeLike/', views.removeLike),
    url(r'^addFollowing/', userViews.addFollowing),
    url(r'^removeFollowing/', userViews.removeFollowing),
    url(r'^profile/', userViews.getProfile),
    url(r'^addComment/', views.addComment),
    url(r'^getFollowers/', userViews.getFollowers),
    url(r'^getNotifications/', userViews.getNotifications),
    url(r'^getComments/', views.getComments),
    url(r'^getPosts/', views.getPosts),
    url(r'^getTrends/', views.getTrends),
    url(r'^addUserTags',views.addUserTags),
    url(r'^getPostDetail',views.getPostDetail),
    url(r'^getPostImage',views.getPostImage),
    url(r'^getProfile',userViews.getProfile),
    url(r'^searchPosts',views.searchPosts)
]
