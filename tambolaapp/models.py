from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from ckeditor.fields import RichTextField

# Create your models here.
class City(models.Model):
    city_name=models.CharField(max_length=100)
    def __str__(self):
        return self.city_name
class User(AbstractUser):
    profile_picture=models.FileField(upload_to ='profile', default='profile/user.png')
    otp=models.CharField(max_length=50,null=True)
    date_of_birth=models.DateField(null=True)
    mobile_no=models.CharField(max_length=50,null=True,unique=True)
    gender=models.CharField(max_length=50,null=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE, null=True)
    refer_by=models.CharField(max_length=100,default='admin')
    refer_code=models.CharField(max_length=50,default=0)
    is_verified=models.BooleanField(default=False)
    is_above18=models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class Game_Rule(models.Model):
    sample_ticket=models.FileField(upload_to ='ticket', default='ticket/sample.png')
    name=models.CharField(max_length=50,null=True,unique=True)
    description=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class NewGame(models.Model):
    game_name=models.CharField(max_length=100,null=True,unique=True)
    message_for_player=models.TextField()
    lobby=models.CharField(max_length=50,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    ticket_cost=models.CharField(max_length=50,default=0)
    start_at=models.DateTimeField()
    ticket_request_till=models.DateTimeField()
    number_of_tickets=models.CharField(max_length=50,null=True)
    timer=models.CharField(max_length=50)
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game_name
    
class RuleInGame(models.Model):
    game=models.ForeignKey(NewGame,on_delete=models.CASCADE, null=True)
    rule=models.ForeignKey(Game_Rule,on_delete=models.CASCADE, null=True)
    price=models.CharField(max_length=50,null=True)
    number_of_tickets=models.CharField(max_length=50,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    total_cost=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now=True)


class HelpAndSupport(models.Model):
    subject=models.CharField(max_length=50)
    description=models.TextField()
    screenshot=models.FileField(upload_to ='helpandsupport', default='helpandsupport/helpandsupport.png')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    
class Page(models.Model):
    title=models.CharField(max_length=50,unique=True)
    content=RichTextField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title