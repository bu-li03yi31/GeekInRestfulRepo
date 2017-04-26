#Created by Yi Li and Yiteng Xu in 2017/04/23
#Modified by Yi Li, Yiteng Xu
#A view where contains all user-relate interfaces (user follow, fetch user profiles, get followers, etc)

from django.shortcuts import render
from GeekInRest.models import Users, Posts, UserTags, Tags, Following, Posts
from GeekInRest.serializers import UserSerializer, PostSerializer
from rest_framework import viewsets
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
import os
import base64
from django.utils import timezone
from django.db.models import Count
from django.db import connection
from django.core import serializers


#Remove a following relationship
@csrf_exempt
def removeFollowing(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        fer = Users.objects.get(email=body['follower'])
        fee = Users.objects.get(email=body['followee'])
        Following.objects.filter(follower=fer, followee=fee).delete()
        return JsonResponse({'result': "true"})
    except Exception as e:
        return JsonResponse({'result': "false", 'message': 'error in addFollowing: ' + str(e)})

#Add a following relationship
@csrf_exempt
def addFollowing(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        fer = Users.objects.get(email=body['follower'])
        fee = Users.objects.get(email=body['followee'])
        following = Following(follower=fer, followee=fee)
        following.save()
        return JsonResponse({'result': "true"})
    except Exception as e:
        return JsonResponse({'result': "false", 'message': 'error in addFollowing: ' + str(e)})

#Get user profile
@csrf_exempt
def getProfile(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        user = body['email']
        #get follower number
        countFollower=Following.objects.filter(followee=user).count() 
        #get following number
        countFollowee=Following.objects.filter(follower=user).count()
        #get posts number
        countPosts=Posts.objects.filter(email=user).count()
        if 'self' in body:
            num_results = Following.objects.filter(follower=body['self'], followee=user).count();
            isFollowing = num_results
            return JsonResponse({'result': "true", "follower_count": str(countFollower), "followee_count": str(countFollowee), "post_count": str(countPosts), "isFollowing": isFollowing})
        else:
            return JsonResponse({'result': "true", "follower_count": str(countFollower), "followee_count": str(countFollowee), "post_count": str(countPosts)})
    except Exception as e:
        return JsonResponse({'result': "false", 'message': 'error in getProfile: ' + str(e)})
    
#Sign up a new user
@csrf_exempt
def createUser(request):
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)
    email = body['email']
    userPassJudge = Users.objects.filter(email=email)
    # print(userPassJudge.get(UserName=username).User_ID)

    if userPassJudge:
        return JsonResponse({'result': "false"})
    else:
        filedir = os.getcwd() + "/users/"
        os.makedirs(os.path.dirname(filedir), exist_ok=True)
        for image in images:
            # filename = os.path.join(dir, "/posts/"+str_time +"/"+ str(i) + ".jpg")
            with open(filedir + email + ".jpg", 'wb') as f:
                f.write(base64.b64decode(image))
            i = i + 1
        data = Users(email=body["email"],password=body["password"],photo=filedir + email + ".jpg",username=body["username"])
        data.save()
        return JsonResponse({'result': "true"})

#Get all followers of one user
@csrf_exempt
def getFollowers(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        cursor = connection.cursor()
        cursor.execute('select u.Photo as photo, u.Username as name from Following f, Users u where f.Follower = u.email and f.Followee = "' + body['email'] + '"')
        rows = cursor.fetchall()
        result = []
        keys = ('photo','username')
        for row in rows:
            result.append(dict(zip(keys,row)))
        json_object = {'data': result, 'result': "true"}
        cursor.close()
        return JsonResponse(json_object)
    except Exception as e:
        return JsonResponse({'result': "false", 'message': 'error in getFollowers: ' + str(e)})


#Get Notifications
@csrf_exempt
def getNotifications(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        cursor = connection.cursor()
        cursor.execute('select u2.Username, tmp.Title, tmp.Timestamp from Users u2, (select l.Email, p.Title, l.Timestamp from Users u, Posts p, Likes l where u.Email=p.Email and p.Pid=l.Pid and u.Email="'+body['email']+'") as tmp where u2.Email=tmp.Email')
        rows = cursor.fetchall()
        keys = ('username','post_title','date')
        #get likes from the query results
        likes = []
        for row in rows:
            likes.append(dict(zip(keys,row)))
        
        #get comments notifications from query results
        cursor.execute('select u2.Username, tmp.Title, tmp.Timestamp from Users u2, (select c.Email, p.Title, c.Timestamp from Users u, Posts p, Comments c where u.Email=p.Email and p.Pid=c.Pid and u.Email="'+body['email']+'") as tmp where u2.Email=tmp.Email')
        rows = cursor.fetchall()
        comments = []
        for row in rows:
            comments.append(dict(zip(keys,row)))
            
        json_object = {'likes': likes, 'result': "true", "comments": comments}
        cursor.close()
        return JsonResponse(json_object)
    except Exception as e:
        return JsonResponse({'result': "false", 'message': 'error in getNotifications: ' + str(e)})
            
