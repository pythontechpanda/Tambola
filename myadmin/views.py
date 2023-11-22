from django.shortcuts import render, redirect
from tambolaapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import datetime
# Create your views here.

def DashboardPage(request):
    notify = User.objects.all().count()
    pending_notify = User.objects.filter(status="Pending").count()
    print(pending_notify)
    return render(request, "index.html", {'notify':notify, 'pending':pending_notify})





def UserTablePage(request):
    get_users = User.objects.all()
    return render(request, "user-table.html", {"get_users":get_users})


def UserCreatePage(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        uname = request.POST["contact"]
        active = request.POST["actv"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        city = request.POST["city"]
        vrfy = request.POST["verificat"]
        above = request.POST["goto"]
        
        birthdate_obj = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))
        
        print("age>>>>>>", age)
        if age >= 18:       
            if User.objects.filter(mobile_no=contact).exists():
                messages.error(request, 'Contact number already taken')
                return redirect('/admin-panel/new-user/')
            else:
                usr = User(first_name=fname, username=uname, is_active=active, mobile_no=contact,date_of_birth=dob, gender=gender, city_id=city,is_verified=vrfy,is_above18=above)
                usr.save()
                return redirect("/admin-panel/users-table/")
        else:
            messages.error(request,"You are not Eligible")
            return redirect('/admin-panel/new-user/')
    else:
        get_city = City.objects.all()
        print("else")
        return render(request, "create-user.html", {"get_city":get_city})
    
        


def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/admin-panel/users-table/")


def EditUser(request, id):
    if request.method == 'POST':
        fname = request.POST["fname"]
        uname = request.POST["contact"]
        active = request.POST["actv"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        cty = request.POST["city"]
        verify = request.POST['verificat']
        yourin = request.POST['goto']
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname, username=uname, is_active=active, mobile_no=contact,date_of_birth=dob, gender=gender, city_id=cty,is_verified=verify,is_above18=yourin)
        messages.success(request, f"{fname}, profile updated successfully")
        return redirect("/admin-panel/users-table/")
    else:
        getUser = User.objects.get(id=id)    
        get_city = City.objects.all()
        return render(request, "edituser.html", {'user':getUser,"get_city":get_city})
    
    
def CityCreate(request):
    if request.method == 'POST':
        ct = request.POST["cty"]
        if City.objects.filter(city_name=ct).exists():
            messages.info(request, 'City already taken')
            return redirect('/admin-panel/city-table/')
        else:
            usr = City(city_name=ct)
            usr.save()
            return redirect("/admin-panel/city-table/")
    else:
        return render(request, "create-city.html")
    
    
    
def CityTablePage(request):
    get_city = City.objects.all()
    return render(request, "city-table.html", {'get_city':get_city})


def DeleteCity(request, id):
    cty = City.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/city-table/")




def EditCity(request, id):
    if request.method == 'POST':
        city = request.POST['cty']        
        uplead = City.objects.filter(id=id)        
        uplead.update(city_name=city)
        messages.success(request, f"{city}, profile updated successfully")
        return redirect("/admin-panel/city-table/") 
    else:
        getCity = City.objects.get(id=id)    
        return render(request, "create-city.html", {'city':getCity})
    
    
    
    
    
    
    
def GameRuleCreate(request):
    if request.method == 'POST':
        samtk = request.POST["sample"]
        nm = request.POST["name"]
        desc = request.POST["desc"]
        usr = request.user.id
        active = request.POST['active']
        
        usr = Game_Rule(sample_ticket=samtk, name=nm, description=desc, user_is=usr, is_active=active)
        usr.save()
        return redirect("/admin-panel/city-table/")
    else:
        return render(request, "create-city.html")
    
    
    
def GameRuleTablePage(request):
    get_rule = Game_Rule.objects.all()
    return render(request, "game-rule-table.html", {'get_rule':get_rule})


def DeleteGameRule(request, id):
    cty = Game_Rule.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/game-rule-table/")



def EditGameRule(request, id):
    if request.method == 'POST':
        city = request.POST['cty']        
        uplead = Game_Rule.objects.filter(id=id)        
        uplead.update(city_name=city)
        messages.success(request, f"{city}, profile updated successfully")
        return redirect("/admin-panel/city-table/") 
    else:
        getCity = Game_Rule.objects.get(id=id)    
        return render(request, "create-city.html", {'city':getCity})