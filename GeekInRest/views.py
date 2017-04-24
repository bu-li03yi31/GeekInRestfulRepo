#Created by Yi Li and Yiteng Xu in 2017/03/23
#Modified by Yi Li, Yiteng Xu and Desheng Zhang

from django.shortcuts import render
from GeekInRest.models import Users, Posts, UserTags, Tags, Likes, Posts
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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

@csrf_exempt
def login(request):
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)
    email = body['email']
    password = body['password']

    userPassJudge = Users.objects.filter(email=email, password=password)
    #print(userPassJudge.get(email=email).password)
    if userPassJudge:

        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})

@csrf_exempt
def user_tags(request):
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)
    tags = body["tags"]
    for tag in tags:
        instance1 = Users.objects.filter(email=email).get(email=email)
        instance2 = Tags.objects.filter(tid=tag).get(tid=tag)
        t = UserTags(email=instance1, tid=instance2)
        t.save()
    return JsonResponse({'result': "true"})

#Create new post
@csrf_exempt
def createNewPost(request):
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)

    str_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    data = Posts(email=body["email"], title=body["title"], content=body["content"],
                        photo="/posts/"+str_time)
    images = body["images"]
    i = 0

    filename=os.getcwd()+"/posts/"+str_time+"/"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    for image in images:
        # filename = os.path.join(dir, "/posts/"+str_time +"/"+ str(i) + ".jpg")
        with open( filename+ str(i) + ".jpg", 'wb') as f:
            f.write(base64.b64decode(image))
        i = i + 1

    data.save()
    return JsonResponse({'result': "true"})

#add like to a post
@csrf_exempt
def addLike(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        str_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        like = Likes(pid=int(body['Pid']), email=body['email'], timestamp=str_time)
        like.save()
        return JsonResponse({'result': "true"})
    except Exception as e:
        return JsonResponse({'result': "false", 'message': 'error in addLike: ' + str(e)})
        
