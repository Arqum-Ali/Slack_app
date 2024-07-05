from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from login.views import MyTokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import *

class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password',]

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'name', 'surname', 'email', 'username', 'password', 'user_kind']
        fields = [ 'id','email']

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    











class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                refresh = MyTokenObtainPairSerializer.get_token(user)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return data
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')
        
# serializers.py
from rest_framework import serializers

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class ChannelMembergetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = ChannelMember
        fields = ['id', 'username', 'joined_at'] 
               
class ChannelMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelMember
        fields = '__all__'
