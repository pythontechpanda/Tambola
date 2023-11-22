from django.shortcuts import render, redirect
from tambolaapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
# Create your views here.

def DashboardPage(request):
    return render(request, "index.html")





def UserTablePage(request):
    get_users = User.objects.all()
    return render(request, "user-table.html", {"get_users":get_users})


def UserCreatePage(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        uname = request.POST["username"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        city = request.POST["city"]
        pwd = request.POST['password']
        
        if User.objects.filter(username=uname).exists():
            messages.info(request, 'Username already taken')
            return redirect('/admin-panel/new-user/')
        else:
            usr = User(first_name=fname, last_name=lname, username=uname, email=email,password=make_password(pwd), mobile_no=contact,date_of_birth=dob, gender=gender, city_id=city,is_verified=False,is_above18=False)
            usr.save()
            return redirect("/admin-panel/users-table/")
    else:
        get_city = City.objects.all()
        return render(request, "create-user.html", {"get_city":get_city})
    
        


def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/admin-panel/users-table/")


def EditUser(request, id):
    if request.method == 'POST':
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        uname = request.POST["username"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        cty = request.POST["city"]
        verify = request.POST['verify']
        above18 = request.POST['above18']
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname, last_name=lname, username=uname, email=email, mobile_no=contact,date_of_birth=dob, gender=gender, city_id=cty,is_verified=verify,is_above18=above18)
        messages.success(request, f"{fname}, profile updated successfully")
        return redirect("/admin-panel/users-table/")
    else:
        getUser = User.objects.get(id=id)    
        get_city = City.objects.all()
        return render(request, "edituser.html", {'user':getUser,"get_city":get_city})
    
    
    
    
    
def CityTablePage(request):
    get_city = City.objects.all()
    return render(request, "city-table.html", {'get_city':get_city})


def DeleteCity(request, id):
    cty = City.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/city-table/")



def EditCity(request, id):
    if request.method == 'POST':
        city = request.POST['city_name']
        
        uplead = City.objects.filter(id=id)
        
        uplead.update(city_name=city)
        messages.success(request, f"{city}, profile updated successfully")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  
    else:
        getUser = User.objects.get(id=id)    
        return render(request, "edituser.html", {'user':getUser})