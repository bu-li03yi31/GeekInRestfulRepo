from django.shortcuts import render
from GeekInRest.models import Users, Posts, UserTags, Tags
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


# Create your views here.
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
def create(request):
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

@csrf_exempt
def newpost1(request):
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)
    # print(time.strftime("%y_%m_%d_%H_%M_%S_%f"))
    # print(datetime.now().strftime("%y_%m_%d_%H_%M_%S_%f"))
    print(os.path.abspath("settings.py"))
    return JsonResponse({'result': "true"})

@csrf_exempt
def newpost(request):
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
