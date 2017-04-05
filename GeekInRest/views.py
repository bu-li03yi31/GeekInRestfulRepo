from django.shortcuts import render
from GeekInRest.models import Users, Posts
from GeekInRest.serializers import UserSerializer, PostSerializer
from rest_framework import viewsets

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
