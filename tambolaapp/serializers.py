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
        fields = ['id','username', 'profile_picture', 'first_name','city','gender','date_of_birth','mobile_no','is_verified','is_above18','device_registration_id','refer_code']
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
        fields = ['id','username', 'profile_picture', 'first_name','city','gender','date_of_birth','mobile_no','is_verified','is_above18','refer_code','refer_by','my_code','otp','tokens']
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
                'refer_code':user.refer_code,
                'refer_by':user.refer_by,
                'my_code':user.my_code,
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
        depth = 1

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class Game_RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game_Rule
        fields = '__all__'
        depth = 2

class NewGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewGame
        fields = '__all__'
        depth = 2
        
class NewGamePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewGame
        fields = '__all__'

class RuleInGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleInGame
        fields = '__all__'
        depth = 2

class HelpAndSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpAndSupport
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class AddMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddMoney
        fields = '__all__'

class WalletAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAdd
        fields = '__all__'

class WalletAmtSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAmt
        fields = '__all__'

class PayByWalletAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayByWalletAmount
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class ComplimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliment
        fields = '__all__'
        depth =2

class ComplimentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliment
        fields = '__all__'

class UpcomingSerializer(serializers.Serializer):
    game_id=serializers.IntegerField()
    game_name=serializers.CharField(max_length=100)
    message_for_player=serializers.CharField(max_length=255)
    lobby=serializers.CharField(max_length=25)
    ticket_cost=serializers.CharField(max_length=25)
    start_at=serializers.DateTimeField()
    ticket_request_till=serializers.DateTimeField()
    number_of_ticket=serializers.IntegerField()
    timer=serializers.CharField(max_length=255)
    private_code=serializers.CharField(max_length=255)
    # game_counter=serializers.CharField(max_length=255)
    is_completed=serializers.BooleanField()
    # created_at=serializers.BooleanField()
    user_id= serializers.IntegerField()
    first_name= serializers.CharField(max_length=255)
    username= serializers.CharField(max_length=255)
    profile_picture=serializers.CharField(max_length=255)
    city=serializers.CharField(max_length=255)
    gender=serializers.CharField(max_length=255)
    date_of_birth=serializers.CharField(max_length=255)
    mobile_no=serializers.CharField(max_length=255)
    is_verified=serializers.BooleanField()
    is_above18=serializers.BooleanField()
    refer_code=serializers.CharField(max_length=255)
    refer_by=serializers.CharField(max_length=255)
    my_code=serializers.CharField(max_length=255)
    played=serializers.IntegerField()
    created=serializers.IntegerField()

class LiveSerializer(serializers.Serializer):
    game_id=serializers.IntegerField()
    game_name=serializers.CharField(max_length=100)
    message_for_player=serializers.CharField(max_length=255)
    lobby=serializers.CharField(max_length=25)
    ticket_cost=serializers.CharField(max_length=25)
    start_at=serializers.DateTimeField()
    ticket_request_till=serializers.DateTimeField()
    number_of_ticket=serializers.IntegerField()
    timer=serializers.CharField(max_length=255)
    private_code=serializers.CharField(max_length=255)
    # game_counter=serializers.CharField(max_length=255)
    is_completed=serializers.BooleanField()
    # created_at=serializers.BooleanField()
    user_id= serializers.IntegerField()
    first_name= serializers.CharField(max_length=255)
    username= serializers.CharField(max_length=255)
    profile_picture=serializers.CharField(max_length=255)
    city=serializers.CharField(max_length=255)
    gender=serializers.CharField(max_length=255)
    date_of_birth=serializers.CharField(max_length=255)
    mobile_no=serializers.CharField(max_length=255)
    is_verified=serializers.BooleanField()
    is_above18=serializers.BooleanField()
    refer_code=serializers.CharField(max_length=255)
    refer_by=serializers.CharField(max_length=255)
    my_code=serializers.CharField(max_length=255)
    played=serializers.IntegerField()
    created=serializers.IntegerField()

class PlayedSerializer(serializers.Serializer):
    game_id=serializers.IntegerField()
    game_name=serializers.CharField(max_length=100)
    message_for_player=serializers.CharField(max_length=255)
    lobby=serializers.CharField(max_length=25)
    ticket_cost=serializers.CharField(max_length=25)
    start_at=serializers.DateTimeField()
    ticket_request_till=serializers.DateTimeField()
    number_of_ticket=serializers.IntegerField()
    timer=serializers.CharField(max_length=255)
    private_code=serializers.CharField(max_length=255)
    # game_counter=serializers.CharField(max_length=255)
    is_completed=serializers.BooleanField()
    # created_at=serializers.BooleanField()
    user_id= serializers.IntegerField()
    first_name= serializers.CharField(max_length=255)
    username= serializers.CharField(max_length=255)
    profile_picture=serializers.CharField(max_length=255)
    city=serializers.CharField(max_length=255)
    gender=serializers.CharField(max_length=255)
    date_of_birth=serializers.CharField(max_length=255)
    mobile_no=serializers.CharField(max_length=255)
    is_verified=serializers.BooleanField()
    is_above18=serializers.BooleanField()
    refer_code=serializers.CharField(max_length=255)
    refer_by=serializers.CharField(max_length=255)
    my_code=serializers.CharField(max_length=255)
    played=serializers.IntegerField()
    created=serializers.IntegerField()

class CreatedSerializer(serializers.Serializer):
    game_id=serializers.IntegerField()
    game_name=serializers.CharField(max_length=100)
    message_for_player=serializers.CharField(max_length=255)
    lobby=serializers.CharField(max_length=25)
    ticket_cost=serializers.CharField(max_length=25)
    start_at=serializers.DateTimeField()
    ticket_request_till=serializers.DateTimeField()
    number_of_ticket=serializers.IntegerField()
    timer=serializers.CharField(max_length=255)
    private_code=serializers.CharField(max_length=255)
    # game_counter=serializers.CharField(max_length=255)
    is_completed=serializers.BooleanField()
    # created_at=serializers.BooleanField()
    user_id= serializers.IntegerField()
    first_name= serializers.CharField(max_length=255)
    username= serializers.CharField(max_length=255)
    profile_picture=serializers.CharField(max_length=255)
    city=serializers.CharField(max_length=255)
    gender=serializers.CharField(max_length=255)
    date_of_birth=serializers.CharField(max_length=255)
    mobile_no=serializers.CharField(max_length=255)
    is_verified=serializers.BooleanField()
    is_above18=serializers.BooleanField()
    refer_code=serializers.CharField(max_length=255)
    refer_by=serializers.CharField(max_length=255)
    my_code=serializers.CharField(max_length=255)
    played=serializers.IntegerField()
    created=serializers.IntegerField()

class ClaimRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimRule
        fields = '__all__'
        depth =2

class ClaimRulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimRule
        fields = '__all__'

class WithdrawRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = '__all__'
        depth =2

class WithdrawRequestPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        depth =2

class NotificationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'
        depth =2

class BankDetailPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'