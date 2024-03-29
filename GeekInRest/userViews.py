#Created by Yi Li and Yiteng Xu in 2017/04/23
#Modified by Yi Li, Yiteng Xu, Desheng Zhang
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
from PIL import Image

#Remove a following relationship
@csrf_exempt
def removeFollowing(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        fer = Users.objects.get(email=body['follower'])
        fee = Users.objects.get(email=body['followee'])
        Following.objects.filter(follower=fer, followee=fee).delete()
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in addFollowing: ' + str(e)})

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
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in addFollowing: ' + str(e)})

#Get user profile
@csrf_exempt
def getProfile(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
	if 'self' in body:
	    self = body['self']
	else:
	    self = None
	user_info = retrieveUserInfo(body['email'],self)
	return JsonResponse(user_info)
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in getProfile: ' + str(e)})

# use email address and self info to retrieve user info
def retrieveUserInfo(user,isSelf):
    try:
        user_name = Users.objects.filter(email=user).get(email=user).username
        # get follower number
        countFollower = Following.objects.filter(followee=user).count()
        # get posts number
        countFollowee = Following.objects.filter(follower=user).count()
        # get post number 
        countPost=Posts.objects.filter(email=user).count()
        # get photo path
        tmp=Users.objects.values('photo').filter(email=user).first()
        if not tmp:
	    path = 'home/ubunt/GeekInProject/users/pikachu.jpg'
	else:
	    path = tmp.get('photo')
	#encode the image
	with open(path,'rb') as imageFile:
	    img = base64.b64encode(imageFile.read())

	# send a dictionary include user infomation
	if isSelf != None:
	    num_results = Following.objects.filter(follower=isSelf,followee=user).count()
            isFollowing = num_results
	    user_info = str({'user_email':str(user),'user_name':str(user_name),'follower_count':countFollower,'followee_count':countFollowee,'post_count':countPost,'isFollowing':isFollowing,'photo':img})
	    return {'result':True,'user_info':user_info}
	else:
	    user_info = str({'user_email':str(user),'user_name':str(user_name),'follower_count':countFollower,'followee_count':countFollowee,'post_count':countPost,'isFollowing':None,'photo':img})
	    return {'result': True,'user_info':user_info}
    except Exception as e:
	return {'result': False, 'message': 'error in getProfile: ' + str(e)}  

#Sign up a new user
@csrf_exempt
def createUser(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
	#if 'password' not in body:
	#    print('has password')
        email = body['email']
        userPassJudge = Users.objects.filter(email=email)
        image = body['image']
        if userPassJudge:
            return JsonResponse({'result': "false"})
        else:
            filedir = os.getcwd() + "/users/"
            with open(filedir + email + ".jpg", 'wb') as f:
                f.write(base64.b64decode(image))
            tmp=Image.open(filedir + email + ".jpg")
            tmp.thumbnail((150,150),Image.ANTIALIAS)
            tmp.save(filedir+email+".jpg", format="JPEG", quality=70)
            data = Users(email=body["email"],password=body["password"],photo=filedir + email + ".jpg",username=body["username"])
            data.save()
            return JsonResponse({'result': True})
    except Exception as e:
	#print('fail')
        #print str(e)
        return JsonResponse({'result': False, 'message': 'error in createUser: ' + str(e)})

#Get all followers of one user
@csrf_exempt
def getFollowers(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        cursor = connection.cursor()
        cursor.execute('select u.Photo, u.Username, u.Email from Following f, Users u where f.Follower=u.email and f.Followee="'+body['email']+'"')
        rows = cursor.fetchall()
        result = []
        keys = ('user_photo','username', 'email')
        for row in rows:
	    row = [str(r) for r in row]
            print(row)
            with open(row[0],'rb') as imageFile:
                row[0] = base64.b64encode(imageFile.read())
            result.append(dict(zip(keys,row)))
        json_object = {'data': result, 'result': True}
        cursor.close()
        return JsonResponse(json_object)
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in getFollowers: ' + str(e)})


@csrf_exempt
def getFollowee(request):
    try:
	json_str = ((request.body).decode('utf-8'))
	body = json.loads(json_str)
	cursor = connection.cursor()
	print(body['email'])
	cursor.execute('select u.Photo, u.Username, u.Email from Following f, Users u where f.Followee=u.email and f.Follower="' + body['email'] + '"')
	rows = cursor.fetchall()
	result = []
	keys = ('user_photo','username','email')
	for row in rows:
	    row = [str(r) for r in row]
	    with open(row[0],'rb') as imageFile:
                row[0] = base64.b64encode(imageFile.read())
	    result.append(dict(zip(keys,row)))
	json_object = {'data':result, 'result': True }
	cursor.close()
	return JsonResponse(json_object)
    except Exception as e:
	return JsonResponse({'result': False, 'message': 'error in getFollowees: ' + str(e)})

#Get Notifications
@csrf_exempt
def getNotifications(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        cursor = connection.cursor()
        query='select u2.Email, u2.Username, tmp.Title, DATE_FORMAT(tmp.TimeStamp,"%m-%d %H:%i") as date, u2.Photo, tmp.Pid, tmp.Photo as p_photo from Users u2, (select p.Pid, l.Email, p.Title, l.Timestamp, p.Photo from Users u, Posts p, Likes l where u.Email=p.Email and p.Pid=l.Pid and u.Email="'+body['email']+'") as tmp where u2.Email=tmp.Email ORDER BY date DESC'
        cursor.execute(query)
        rows = cursor.fetchall()
        #get likes from the query results 
        likes = []
        for row in rows:
            user_email=row[0]
            username=row[1]
            title=row[2]
            date=row[3]
            u_path=row[4]
            pid=row[5]
            p_path=row[6]+'cover.jpg'
            with open(u_path,'rb') as imageFile:
                u_img=base64.b64encode(imageFile.read())
            with open(p_path,'rb') as imageFile:
                p_img=base64.b64encode(imageFile.read())
            likes.append({'username':username, 'email':user_email, 'title':title, 'date':date, 'user_photo':u_img, 'pid':int(pid), 'post_cover':p_img})
        #get comments notifications from query results
        query='select u2.Email, u2.Username, tmp.Title, DATE_FORMAT(tmp.TimeStamp,"%m-%d %H:%i") as date, u2.Photo, tmp.Pid, tmp.Photo as p_photo from Users u2, (select p.Pid, c.Email, p.Title, c.Timestamp, p.Photo from Users u, Posts p, Comments c where u.Email=p.Email and p.Pid=c.Pid and u.Email="'+body['email']+'") as tmp where u2.Email=tmp.Email ORDER BY date DESC'
        cursor.execute(query)
        rows = cursor.fetchall()
        comments = []
        for row in rows:
            user_email=row[0]
            username=row[1]
            title=row[2]
            date=row[3]
            u_path=row[4]
            pid=row[5]
            p_path=row[6]+'cover.jpg'
            with open(u_path,'rb') as imageFile:
                u_img=base64.b64encode(imageFile.read())
            with open(p_path,'rb') as imageFile:
                p_img=base64.b64encode(imageFile.read())
            comments.append({'username':username, 'email':user_email, 'title':title, 'date':date, 'user_photo':u_img, 'pid':int(pid), 'post_cover':p_img})
        json_object = {'likes': likes, 'result': True, "comments": comments}
        cursor.close()
        return JsonResponse(json_object)
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in getNotifications: ' + str(e)})
            
