from rest_framework import serializers
from GeekInRest.models import Users, Posts

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'email')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ('title', 'email', 'content')
