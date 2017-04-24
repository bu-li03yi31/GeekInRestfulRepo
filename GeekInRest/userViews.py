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


#Add a following relationship
@csrf_exempt
def addFollowing(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        str_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        following = Following(follower=body['follower'], followee=body['followee'], timestamp=str_time)
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
        follower_query=Following.objects.filter(followee=user).annotate(num_followers=Count('Follower',distinct=True))
        countFollower = follower_query.num_followers
        #get following number
        followee_query=Following.objects.filter(follower=user).annotate(num_followees=Count('Followee',distinct=True))
        countFollowee = followee_query.num_followees
        #get posts number
        post_query=Posts.objects.filter(email=user).annotate(num_posts=Count('Pid', distinct=True))
        countPosts=post_query.num_posts
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


