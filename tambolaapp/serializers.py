from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import random

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'profile_picture', 'first_name','city','gender','date_of_birth','mobile_no','is_verified','is_above18']
    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()
    otp = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    def get_otp(self, obj):
        randomNumber = random.randint(1000, 9999)
        return randomNumber
    class Meta:
        model = User
        fields = ['id','username', 'profile_picture', 'first_name','city','gender','date_of_birth','mobile_no','is_verified','is_above18','otp','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        # password = attrs.get('password','')
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                raise AuthenticationFailed('Account disabled, contact admin')
            if not user.is_above18:
                raise AuthenticationFailed('Age must be minimum of 18 years')
            return {
                'id': user.id,
                'first_name': user.first_name,
                'username': user.username,
                'profile_picture':user.profile_picture,
                'city':user.city,
                'gender':user.gender,
                'date_of_birth':user.date_of_birth,
                'mobile_no':user.mobile_no,
                'is_verified':user.is_verified,
                'is_above18':user.is_above18,
                'tokens': user.tokens
            }
        except:
            raise AuthenticationFailed('Invalid credentials, try again')

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class Game_RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game_Rule
        fields = '__all__'

class NewGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewGame
        fields = '__all__'

class RuleInGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleInGame
        fields = '__all__'