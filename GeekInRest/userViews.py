#Created by Yi Li and Yiteng Xu in 2017/04/23
#Modified by Yi Li, Yiteng Xu

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

#Add a following relationship
@csrf_exempt
def addFollowing(request):
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)
