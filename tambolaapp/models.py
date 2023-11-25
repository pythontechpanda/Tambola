from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from ckeditor.fields import RichTextField
import datetime
import os
import string
import random

# Create your models here.
class City(models.Model):
    city_name=models.CharField(max_length=100)
    def __str__(self):
        return self.city_name
    



N = 7
res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
var =str(res)


def filepath_profile(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('profile/', filename)

class User(AbstractUser):
    STATUS = (
        ('Pending', 'Pending'),
        ('Read', 'Read'),
    )
    profile_picture=models.FileField(upload_to=filepath_profile, default='profile/user.png')
    otp=models.CharField(max_length=50,null=True)
    date_of_birth=models.DateField(null=True)
    mobile_no=models.CharField(max_length=50,null=True,unique=True)
    gender=models.CharField(max_length=50,null=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE,null=True)
    my_code=models.CharField(max_length=100,default=var)
    refer_by=models.CharField(max_length=100,default='admin')
    refer_code=models.CharField(max_length=50,default=0)
    is_verified=models.BooleanField(default=False)
    is_above18=models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS)
    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    class Meta:
        db_table="customer"


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('ticket/', filename)

class Game_Rule(models.Model):
    sample_ticket=models.FileField(upload_to =filepath, default='ticket/sample.png')
    name=models.CharField(max_length=50,null=True,unique=True)
    description=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


game_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
game_code_var =str(game_code)
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
    private_code=models.CharField(max_length=100,default=game_code_var)
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
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title



class AddMoney(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now=True)
    add_status = models.BooleanField(default=False)
    add_price = models.CharField(max_length=200, null=True)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

class WalletAdd(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    walletamount=models.IntegerField()
    wallettime=models.DateTimeField(auto_now_add=True)
    walletstatus=models.BooleanField(default=False)

class WalletAmt(models.Model):
    walt = models.ForeignKey(WalletAdd,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    use_date = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    amount = models.CharField(max_length=200, null=True)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

class PayByWalletAmount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    walletid = models.CharField(max_length=100)
    
    
    
class Ticket(models.Model):
    assign_to=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    game=models.ForeignKey(NewGame,on_delete=models.CASCADE)
    value=models.JSONField(default=[])
    is_winner=models.BooleanField(default=False)
    is_paid=models.BooleanField(default=False)

class BuyTicket(models.Model):
    ticketid = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    orderdate = models.DateTimeField(auto_now=True)
    order_status = models.BooleanField(default=False)
    order_price = models.CharField(max_length=200, null=True)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)
    