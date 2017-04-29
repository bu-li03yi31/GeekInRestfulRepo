#Created by Yi Li and Yiteng Xu in 2017/03/23
#Modified by Yi Li, Yiteng Xu and Desheng Zhang

from django.shortcuts import render
from django.shortcuts import HttpResponse
from GeekInRest.models import Users, Posts, UserTags, Tags, Likes, Posts, Comments
from GeekInRest.serializers import UserSerializer, PostSerializer
from rest_framework import viewsets
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection
from datetime import datetime
import os
import base64
import ast
import unicodedata
from GeekInRest import userViews
import glob
from django.utils import timezone
import os
from PIL import Image

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
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        email = body['email']
        password = body['password']
	if 'self' in body:
	    self = True
	else:
	    self = False
        userIsLogedIn = Users.objects.filter(email=email, password=password)
       # print(userPassJudge.get(email=email).password)
        if userIsLogedIn:
            #return JsonResponse({'result': True})
	    userInfo = userViews.retrieveUserInfo(email,self)
	    #print()
	    if 'user_info' in userInfo:
	        print('has user info')
	    if 'message' in userInfo:
		print(userInfo['message'])

	    return JsonResponse(userInfo)
        else:
            return JsonResponse({'result': False,'message':'user haven\'t logged in'})
    except Exception as e:
        return JsonResponse({'result':False,'message':'error in login: ' + str(e)})
    
@csrf_exempt
def addUserTags(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        tags = body["tags"]
	tags = unicodedata.normalize('NFKD', tags).encode('ascii','ignore')
        tags = tags[1:-1].split(',')
        email = body["email"]
        for tag in tags:
	    tag = tag.rstrip()
	    print(tag)
            user_email = Users.objects.filter(email=email).get(email=email)
            user_tag = Tags.objects.filter(tag=tag).get(tag=tag)
            t = UserTags(email=user_email, tid=user_tag)
            t.save()
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result':False,'message':'error in addUserTags: ' + str(e)})

#Create new post
@csrf_exempt
def createNewPost(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)

        str_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        user_email = Users.objects.get(email=body["email"])
        filename=os.getcwd()+"/posts/"+body["email"]+"_"+str_time+"/"
        data = Posts(email=user_email, title=body["title"], content=body["content"],photo=filename)
        images = body["images"]
        i = 0
        os.makedirs(os.path.dirname(filename))

        for image in images:
            # filename = os.path.join(dir, "/posts/"+str_time +"/"+ str(i) + ".jpg")
            with open( filename+ str(i) + ".jpg", 'wb') as f:
                f.write(base64.b64decode(image))
            i = i + 1
        data.save()
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in createNewPost: ' + str(e)})
    
#add like to a post
@csrf_exempt
def addLike(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        post = Posts.objects.get(pid=int(body['pid']))
        user = Users.objects.get(email=body['email'])
        like = Likes(pid=post, email=user)
        like.save()
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in addLike: ' + str(e)})

#remove like to a post
@csrf_exempt
def removeLike(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        post = Posts.objects.get(pid=int(body['pid']))
        user = Users.objects.get(email=body['email'])
        Likes.objects.filter(pid=post, email=user).delete()
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in addLike: ' + str(e)})

#add comment to a post
@csrf_exempt
def addComment(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        #Since Pid in Comments is foreign key of Pid in Posts,
        #pid in comment object must be given a Posts object
        post = Posts.objects.get(pid=int(body['pid']))
        comment = Comments(email=body['email'], content=body['content'], pid=post)
        comment.save()
        return JsonResponse({'result': True})
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in addComment: ' + str(e)})


#get comments of a post
@csrf_exempt
def getComments(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        pid=int(body['pid'])
        cursor = connection.cursor()
        cursor.execute('select p.Pid, u.Username, u.Photo, c.Email, c.Content, DATE_FORMAT(c.TimeStamp,"%m-%d %H:%i") from Users u, Comments c, Posts p where p.Pid=c.Pid and u.Email=c.Email and p.Pid=' + str(pid))
        rows = cursor.fetchall()
        #keys = ('pid','username','photo','email','content','date')
        res = []
        for row in rows:
            #res.append(dict(zip(keys,row)))
            username=row[1]
            path=row[2]
            user_email=row[3]
            content=row[4]
            date=row[5]
            with open(path,'rb') as imageFile:
                img=base64.b64encode(imageFile.read())
            res.append({'username':username, 'user_photo':img, 'content':content, 'date':date, 'email':user_email})
        json_object = {'data': res, 'result': True}
        cursor.close()
        return JsonResponse(json_object)
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in getComments: ' + str(e)})


#get posts of a email
@csrf_exempt
def getPosts(request):
    try:
        json_str = ((request.body).decode('utf-8'))
        body = json.loads(json_str)
        page=int(body['page'])
        cursor = connection.cursor()
        cursor.execute('select u.Photo as u_photo, u.Username, p.Title, p.Photo as p_photo, p.Pid  from Users u, Posts p where u.Email=p.Email and u.Email="'+body['email']+'" limit '+str(6*page)+','+str(6*page+5))
        rows=cursor.fetchall()
        res = []
        for row in rows:
            username=row[1]
            title=row[2]
            path=row[3]+'/0.jpg'
            with open(path,'rb') as imageFile:
                p_img=base64.b64encode(imageFile.read())
            path=row[0]
            with open(path,'rb') as imageFile:
                u_img=base64.b64encode(imageFile.read())
            res.append({'pid':int(row[4]), 'username':username, 'title':title, 'post_cover':p_img, 'user_photo':u_img})
        json_object = {'data': res, 'result': True}
        cursor.close()
        return JsonResponse(json_object)
    except Exception as e:
        return JsonResponse({'result': False, 'message': 'error in getPosts: ' + str(e)})

@csrf_exempt
def getPostDetail(request):
    try:
	json_str = ((request.body).decode('utf-8'))
	body = json.loads(json_str)
	post_object = Posts.objects.get(pid = body['pid'])
	user_email = post_object.email.email
	user_name = post_object.email.username
	star_num = Likes.objects.filter(pid = post_object).count()
	comment_num = Comments.objects.filter(pid = post_object).count()
	post_photo_path = post_object.photo
	post_photo_list = getPhotoList(post_photo_path)
	path = Users.objects.values('photo').filter(email=user_email).first().get('photo')
        isLiked = Likes.objects.filter(pid=post_object, email=Users.objects.get(email=body['email'])).count()
	with open(path,'rb') as imageFile:
            img = base64.b64encode(imageFile.read())
        print path
	data = {'pid':body['pid'],'user_email':user_email,'user_name':user_name,'user_photo':img,'comment_count':comment_num,'star_count':star_num,'title':post_object.title,'content':post_object.content,'photos':post_photo_list, 'isLiked': int(isLiked)}
	return JsonResponse({'result':True,'data':data})
    except Exception as e:
	return JsonResponse({'result': False, 'message': 'error in getPostDetail: ' + str(e)})


@csrf_exempt
def getPostImage(request):
    try:
	path = request.get_full_path()[13:]
	print(path)
	with open(path,'rb') as img:
	    return HttpResponse(img.read(),content_type="image/jpg")
    except IOError:
        red  = Image.new('RGBA',(1,1),(255,0,0))
        response = HttpResponse(content_type="image/jpg")
        red.save(response,"JPEG")
        return response

def getPhotoList(path):
    try:
        return [str(path+f) for f in os.listdir(path) if f.endswith('.jpg')]
    except Exception as e:
	return esonResponse({'result': False, 'message': 'error in getPostList: ' + str(e)})
	
