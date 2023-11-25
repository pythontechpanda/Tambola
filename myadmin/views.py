from django.shortcuts import render, redirect
from tambolaapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import datetime
# Create your views here.
import os
from . forms import *
from django.contrib.auth.decorators import login_required


def Login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin-panel/index/')            
        else:
            messages.error(request, "Username or password incorrect")
            return redirect('/admin-panel/')   
    else:
        return render(request, "page-login.html")


def logout_call(request):
    logout(request)
    return redirect('/admin-panel/')


@login_required(login_url="/admin-panel/")
def DashboardPage(request):
    notify = User.objects.all().count()
    pending_notify = User.objects.filter(status="Pending").count()
    print(pending_notify)
    return render(request, "index.html", {'notify':notify, 'pending':pending_notify})


# def ViewAdminProfile(request, id):
#     user = User.objects.get(id=id)
#     return render(request, "admin-profile.html", {'user':user})

@login_required(login_url="/admin-panel/")
def UserTablePage(request):
    get_users = User.objects.all()
    return render(request, "user-table.html", {"get_users":get_users})

@login_required(login_url="/admin-panel/")
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
        profile = request.FILES['profile_pic']
        
        birthdate_obj = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))
        
        print("age>>>>>>", age)
        if age >= 18:       
            if User.objects.filter(mobile_no=contact).exists():
                messages.error(request, 'Contact number already taken')
                return redirect('/admin-panel/new-user/')
            else:
                usr = User(first_name=fname, username=uname, is_active=active, profile_picture=profile, mobile_no=contact,date_of_birth=dob, gender=gender, city_id=city,is_verified=vrfy,is_above18=above)
                usr.save()
                return redirect("/admin-panel/users-table/")
        else:
            messages.error(request,"You are not Eligible")
            return redirect('/admin-panel/new-user/')
    else:
        get_city = City.objects.all()
        print("else")
        return render(request, "create-user.html", {"get_city":get_city})
    
        

@login_required(login_url="/admin-panel/")
def DeleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/admin-panel/users-table/")

@login_required(login_url="/admin-panel/")
def EditUser(request, id):
    upleid = User.objects.get(id=id)
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
        
        
        if len(request.FILES) !=0:
            if len(upleid.profile_picture) > 0:
                os.remove(upleid.profile_picture.path)
                print(upleid.profile_picture.path)
            upleid.profile_picture = request.FILES['profile_pic']
            
            upleid.save()
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname, username=uname, is_active=active, mobile_no=contact,date_of_birth=dob, gender=gender, city_id=cty,is_verified=verify,is_above18=yourin)
        messages.success(request, f"{fname}, profile updated successfully")
        return redirect("/admin-panel/users-table/")
    else:
        getUser = User.objects.get(id=id)    
        get_city = City.objects.all()
        return render(request, "edituser.html", {'user':getUser,"get_city":get_city})
    
    
@login_required(login_url="/admin-panel/") 
def ForgotPassword(request,id):
    print('id',id)
    oldpwd=User.objects.get(id=id)
    print('id',oldpwd.id)
    print('kdfjv',oldpwd.password)
    if request.method == "POST":
        newpwd = request.POST['newpassword']
        print(newpwd)
        uplead = User.objects.filter(id=id)
        print("working...............")
        uplead.update(password=make_password(newpwd))
        messages.success(request,"Password changed")
        logout(request)
        return redirect('/admin-panel/')
    else:
        edtad=User.objects.get(id=id)
        print(edtad)
        return render(request,'change-password.html',{'edtad':edtad, 'oldpwd':oldpwd})
    
@login_required(login_url="/admin-panel/")
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
    
    
@login_required(login_url="/admin-panel/")
def CityTablePage(request):
    get_city = City.objects.all()
    return render(request, "city-table.html", {'get_city':get_city})

@login_required(login_url="/admin-panel/")
def DeleteCity(request, id):
    cty = City.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/city-table/")



@login_required(login_url="/admin-panel/")
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
    
    
    
    
    
    
@login_required(login_url="/admin-panel/")    
def GameRuleCreate(request):
    if request.method == 'POST':
        samtk = request.FILES["smp_img"]
        nm = request.POST["rul_nm"]
        desc = request.POST["desc"]        
        active = request.POST['actv']
        
        usr = Game_Rule(sample_ticket=samtk, name=nm, description=desc, is_active=active)
        usr.save()
        return redirect("/admin-panel/game-rule-table/")
    else:
        return render(request, "create-game-rule.html")
    
    
@login_required(login_url="/admin-panel/")    
def GameRuleTablePage(request):
    get_rule = Game_Rule.objects.all()
    return render(request, "game-rule-table.html", {'get_rule':get_rule})

@login_required(login_url="/admin-panel/")
def DeleteGameRule(request, id):
    cty = Game_Rule.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/game-rule-table/")


@login_required(login_url="/admin-panel/")
def EditGameRule(request, id):
    upleid = Game_Rule.objects.get(id=id)
    if request.method == 'POST':
        nm = request.POST["rul_nm"]
        desc = request.POST["desc"]        
        active = request.POST['actv']
        
        if len(request.FILES) !=0:
            if len(upleid.sample_ticket) > 0:
                os.remove(upleid.sample_ticket.path)
                print(upleid.sample_ticket.path)
            upleid.sample_ticket = request.FILES['smp_img']
            
            upleid.save()      
        uplead = Game_Rule.objects.filter(id=id)        
        uplead.update(name=nm, description=desc, is_active=active)
        messages.success(request, "Game rule updated successfully")
        return redirect("/admin-panel/game-rule-table/") 
    else:
        getRule = Game_Rule.objects.get(id=id)    
        return render(request, "edit-game-rule.html", {'rule':getRule})
    
    
@login_required(login_url="/admin-panel/")   
def NewGameCreate(request):
    if request.method == 'POST':
        gn = request.POST["gname"]
        mfp = request.POST["message"]
        lob = request.POST["lobby"]        
        usr = request.POST["user"]
        tc = request.POST["tkcost"]
        sa = request.POST["start"]
        trt = request.POST["tkrequest"]
        noft = request.POST["noftk"]
        tr = request.POST["tim"]
        pc = request.POST["pcode"]
        ic = request.POST["actv"]
        
        
        usr = NewGame(game_name=gn, message_for_player=mfp, lobby=lob, user_id=usr, ticket_cost=tc, start_at=sa,ticket_request_till=trt, number_of_tickets=noft,timer=tr, private_code=pc, is_completed=ic, created_at=datetime.datetime.now())
        usr.save()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>: ",usr.number_of_tickets, usr.id)
        for tick in range(int(usr.number_of_tickets)):
            print("ticket", tick)
            def column_elements():
                c=0
                column=[]
                for i in range(1,10):
                    rn=random.randrange(1,3)
                    c+=rn
                    column.append(rn)
                if c==15:
                    return column
                else:
                    return column_elements()
            col=column_elements()
            print('col',col)
            def row_elements(column_list):
                columns=[]
                for i,j in zip(column_list,range(1,len(column_list)+1)):
                    row=[]
                    inputNumbers = range((j*10+1)-10,j*10)
                    row=random.sample(inputNumbers, i)
                    row.sort()
                    columns.append(row)
                return columns

            rw=row_elements(col)
            print('rw',rw)

            tk=Ticket(game_id=usr.id,assign_to_id=1,value=rw)
            tk.save()
            print("Object Saved.......")
        return redirect("/admin-panel/new-game-table/")
    else:
        getUser = User.objects.all()
        return render(request, "create-game.html", {'getUser':getUser})
    
    
@login_required(login_url="/admin-panel/")    
def NewGameTablePage(request):
    get_game = NewGame.objects.all()
    return render(request, "game-table.html", {'get_game':get_game})

@login_required(login_url="/admin-panel/")
def DetailNewGame(request, id):
    get_game = NewGame.objects.get(id=id)
    return render(request, "game-detail.html", {'get_game':get_game})

@login_required(login_url="/admin-panel/")
def DeleteNewGame(request, id):
    cty = NewGame.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/new-game-table/")


@login_required(login_url="/admin-panel/")
def EditNewGame(request, id):
    if request.method == 'POST':
        gn = request.POST["gname"]
        mfp = request.POST["message"]
        lob = request.POST["lobby"]        
        usr = request.POST["user"]
        tc = request.POST["tkcost"]
        # sa = request.POST["start"]
        # trt = request.POST["tkrequest"]
        noft = request.POST["noftk"]
        tr = request.POST["tim"]
        pc = request.POST["pcode"]
        ic = request.POST["actv"]
        
          
        uplead = NewGame.objects.filter(id=id)        
        uplead.update(game_name=gn, message_for_player=mfp, lobby=lob, user_id=usr, ticket_cost=tc, number_of_tickets=noft,timer=tr, private_code=pc, is_completed=ic)
        messages.success(request, "Game updated successfully")
        return redirect("/admin-panel/new-game-table/") 
    else:
        getGame = NewGame.objects.get(id=id)    
        return render(request, "edit-game.html", {'game':getGame})
    
    
    
@login_required(login_url="/admin-panel/")   
def RuleInGameCreate(request):
    if request.method == 'POST':
        samtk = request.POST["game"]
        nm = request.POST["rule"]
        price = request.POST["price"]        
        noft = request.POST['number_of_tickets']
        usr = request.POST['user']
        tc = request.POST['total_cost']
        
        usr = RuleInGame(game_id=samtk, rule_id=nm, price=price, number_of_tickets=noft, user_id=usr, total_cost=tc, created_at=datetime.now())
        usr.save()
        return redirect("/admin-panel/rule-in-game-table/")
    else:
        getUser = User.objects.all()
        getGame = NewGame.objects.all()
        getRule = Game_Rule.objects.all()
        return render(request, "create-rule-in-game.html", {'getUser':getUser,'getGame':getGame,'getRule':getRule})
    
    
@login_required(login_url="/admin-panel/")   
def RuleInGameTablePage(request):
    get_rule = RuleInGame.objects.all()
    return render(request, "rule-in-game-table.html", {'get_rule':get_rule})

@login_required(login_url="/admin-panel/")
def DetailRuleInGame(request, id):
    get_game = RuleInGame.objects.get(id=id)
    return render(request, "rule-in-game-detail.html", {'get_game':get_game})

@login_required(login_url="/admin-panel/")
def DeleteRuleInGame(request, id):
    cty = RuleInGame.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/rule-in-game-table/")


@login_required(login_url="/admin-panel/")
def EditRuleInGame(request, id):
    if request.method == 'POST':
        samtk = request.POST["game"]
        nm = request.POST["rule"]
        price = request.POST["price"]        
        noft = request.POST['number_of_tickets']
        usr = request.POST['user']
        tc = request.POST['total_cost']
        
         
        uplead = RuleInGame.objects.filter(id=id)        
        uplead.update(game_id=samtk, rule_id=nm, price=price, number_of_tickets=noft, user_id=usr, total_cost=tc, created_at=datetime.now())
        messages.success(request, "Game rule updated successfully")
        return redirect("/admin-panel/rule-in-game-table/") 
    else:
        getRulein = RuleInGame.objects.get(id=id)  
        getUser = User.objects.all()
        getGame = NewGame.objects.all()
        getRule = Game_Rule.objects.all()  
        
        return render(request, "edit-rule-in-game.html", {'get_rl':getRulein,'getUser':getUser,'getGame':getGame,'getRule':getRule})
    
    
    
@login_required(login_url="/admin-panel/")  
def HelpAndSupportCreate(request):
    if request.method == 'POST':
        samtk = request.FILES["screenshot"]
        nm = request.POST["subject"]
        desc = request.POST["description"]        
        usr = request.POST['user']
        
        usr = HelpAndSupport(screenshot=samtk, subject=nm, description=desc, user_id=usr, created_at=datetime.now())
        usr.save()
        return redirect("/admin-panel/help-support-table/")
    else:
        getUser = User.objects.all()
        return render(request, "create-help-support.html",{'getUser':getUser})
    
    
@login_required(login_url="/admin-panel/")    
def HelpAndSupportTablePage(request):
    get_rule = HelpAndSupport.objects.all()
    return render(request, "help-support-table.html", {'get_rule':get_rule})

@login_required(login_url="/admin-panel/")
def DeleteHelpAndSupport(request, id):
    cty = HelpAndSupport.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/help-support-table/")


@login_required(login_url="/admin-panel/")
def EditHelpAndSupport(request, id):
    upleid = HelpAndSupport.objects.get(id=id)
    if request.method == 'POST':
        nm = request.POST["subject"]
        desc = request.POST["description"]        
        usr = request.POST['user']
        
        if len(request.FILES) !=0:
            if len(upleid.screenshot) > 0:
                os.remove(upleid.screenshot.path)
                print(upleid.screenshot.path)
            upleid.screenshot = request.FILES['screenshot']
            
            upleid.save()      
        uplead = HelpAndSupport.objects.filter(id=id)        
        uplead.update(subject=nm, description=desc, user_id=usr)
        messages.success(request, "Help Support updated successfully")
        return redirect("/admin-panel/help-support-table/") 
    else:
        getHelp = HelpAndSupport.objects.get(id=id)    
        getUser = User.objects.all()
        return render(request, "edit-help-support.html", {'getHelp':getHelp,'getUser':getUser})
    
    
    
    
    
    

@login_required(login_url="/admin-panel/")
def PageCreate(request):
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/admin-panel/page-table/')
    else:
        form = PageForm()
        
    context = {
        "form":form
    }
    return render(request, "create-page.html",context)


@login_required(login_url="/admin-panel/")
def PageTablePage(request):
    get_rule = Page.objects.all()
    return render(request, "page-table.html", {'get_rule':get_rule})

@login_required(login_url="/admin-panel/")
def DeletePage(request, id):
    cty = Page.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/page-table/")

@login_required(login_url="/admin-panel/")
def PageUpdate(request, id):
    if request.method == 'POST':
        
        uplead = Page.objects.get(id=id)
        form = PageForm(request.POST, request.FILES, instance=uplead)
        if form.is_valid():
            form.save()
        return redirect('/admin-panel/page-table/')
    else:
        getdata = Page.objects.get(id=id)
        form = PageForm(instance=getdata)
        return render(request, "edit-page.html", {'form':form})
    




@login_required(login_url="/admin-panel/")
def AddMoneyCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["actv"]
        lob = request.POST["add_price"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"]        
        
        
        usr = AddMoney(user_id=gn, add_status=mfp, add_price=lob, razor_pay_order_id=rpoi, razor_pay_payment_id=tc, razor_pay_payment_signature=sa)
        usr.save()
        return redirect("/admin-panel/add-money-table/")
    else:
        getUser = User.objects.all()
        return render(request, "create-addmoney.html", {'getUser':getUser})
    
    
@login_required(login_url="/admin-panel/")   
def AddMoneyTablePage(request):
    get_money = AddMoney.objects.all()
    return render(request, "add-money-table.html", {'get_money':get_money})

@login_required(login_url="/admin-panel/")
def DetailAddMoney(request, id):
    get_money = AddMoney.objects.get(id=id)
    return render(request, "add-money-detail.html", {'get_game':get_money})

@login_required(login_url="/admin-panel/")
def DeleteAddMoney(request, id):
    cty = AddMoney.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/add-money-table/")


@login_required(login_url="/admin-panel/")
def EditAddMoney(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["actv"]
        lob = request.POST["add_price"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"]   
        
          
        uplead = AddMoney.objects.filter(id=id)        
        uplead.update(user_id=gn, add_status=mfp, add_price=lob, razor_pay_order_id=rpoi, razor_pay_payment_id=tc, razor_pay_payment_signature=sa)
        messages.success(request, "AddMoney updated successfully")
        return redirect("/admin-panel/add-money-table/") 
    else:
        getMoney = AddMoney.objects.get(id=id)    
        getUser = User.objects.all()
        return render(request, "edit-addmoney.html", {'money':getMoney, 'getUser':getUser})
    
    
    


@login_required(login_url="/admin-panel/")
def WalletAddCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletamount"]     
        rpoi = request.POST["actv"]      
        
        
        usr = WalletAdd(user_id=gn, walletamount=mfp, walletstatus=rpoi)
        usr.save()
        return redirect("/admin-panel/wallet-add-table/")
    else:
        getUser = User.objects.all()
        return render(request, "create-wallet-add.html", {'getUser':getUser})
    
    
@login_required(login_url="/admin-panel/")   
def WalletAddTablePage(request):
    get_wallet = WalletAdd.objects.all()
    return render(request, "wallet-add-table.html", {'get_wallet':get_wallet})

@login_required(login_url="/admin-panel/")
def DeleteWalletAdd(request, id):
    cty = WalletAdd.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/wallet-add-table/")


@login_required(login_url="/admin-panel/")
def EditWalletAdd(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletamount"]     
        rpoi = request.POST["actv"]
        
          
        uplead = WalletAdd.objects.filter(id=id)        
        uplead.update(user_id=gn, walletamount=mfp, walletstatus=rpoi)
        messages.success(request, "Wallet add updated successfully")
        return redirect("/admin-panel/wallet-add-table/") 
    else:
        getWallet = WalletAdd.objects.get(id=id)    
        getUser = User.objects.all()
        return render(request, "edit-wallet-add.html", {'getWallet':getWallet, 'getUser':getUser})
    
    
@login_required(login_url="/admin-panel/")   
def WalletAmtCreate(request):
    if request.method == 'POST':
        wa = request.POST["walt"]
        gn = request.POST["user"]
        apy_st = request.POST["actv"]
        amt = request.POST["amount"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"]       
        
        
        usr = WalletAmt(walt_id=wa, user_id=gn, payment_status=apy_st, amount=amt,razor_pay_order_id=rpoi,razor_pay_payment_id=tc,razor_pay_payment_signature=sa)
        usr.save()
        return redirect("/admin-panel/wallet-amount-table/")
    else:
        getWallet = WalletAdd.objects.all()
        getUser = User.objects.all()
        return render(request, "create-wallet-amount.html", {'getUser':getUser,'getWallet':getWallet})
    
    
@login_required(login_url="/admin-panel/")    
def WalletAmtTablePage(request):
    get_wallet = WalletAmt.objects.all()
    return render(request, "wallet-amount-table.html", {'get_wallet':get_wallet})

@login_required(login_url="/admin-panel/")
def DetailWalletAmt(request, id):
    get_wallet = WalletAmt.objects.get(id=id)
    return render(request, "wallet-amount-detail.html", {'get_wallet':get_wallet})

@login_required(login_url="/admin-panel/")
def DeleteWalletAmt(request, id):
    cty = WalletAmt.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/wallet-amount-table/")


@login_required(login_url="/admin-panel/")
def EditWalletAmt(request, id):
    if request.method == 'POST':
        wa = request.POST["walt"]
        gn = request.POST["user"]
        apy_st = request.POST["actv"]
        amt = request.POST["amount"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"] 
        
          
        uplead = WalletAmt.objects.filter(id=id)        
        uplead.update(walt_id=wa, user_id=gn, payment_status=apy_st, amount=amt,razor_pay_order_id=rpoi,razor_pay_payment_id=tc,razor_pay_payment_signature=sa)
        messages.success(request, "Wallet amount updated successfully")
        return redirect("/admin-panel/wallet-amount-table/") 
    else:
        getWalletadd = WalletAdd.objects.all()
        getWallet = WalletAmt.objects.get(id=id)    
        getUser = User.objects.all()
        return render(request, "edit-wallet-amount.html", {'getWallet':getWallet, 'getUser':getUser,'getWalletadd':getWalletadd})
    
    
    
    
@login_required(login_url="/admin-panel/")   
def PayByWalletAmountCreate(request):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletid"]      
        
        
        usr = PayByWalletAmount(user_id=gn, walletid=mfp)
        usr.save()
        return redirect("/admin-panel/pay-by-wallet-table/")
    else:
        getUser = User.objects.all()
        return render(request, "create-payby-wallet.html", {'getUser':getUser})
    
    
@login_required(login_url="/admin-panel/")   
def PayByWalletAmountTablePage(request):
    get_wallet = PayByWalletAmount.objects.all()
    return render(request, "pay-by-wallet-table.html", {'get_wallet':get_wallet})

@login_required(login_url="/admin-panel/")
def DeletePayByWalletAmount(request, id):
    cty = PayByWalletAmount.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/pay-by-wallet-table/")


@login_required(login_url="/admin-panel/")
def EditPayByWalletAmount(request, id):
    if request.method == 'POST':
        gn = request.POST["user"]
        mfp = request.POST["walletid"]   
        
          
        uplead = PayByWalletAmount.objects.filter(id=id)        
        uplead.update(user_id=gn, walletid=mfp)
        messages.success(request, "Pay by wallet updated successfully")
        return redirect("/admin-panel/pay-by-wallet-table/") 
    else:
        getWallet = PayByWalletAmount.objects.get(id=id)    
        getUser = User.objects.all()
        return render(request, "edit-pay-by-wallet.html", {'getWallet':getWallet, 'getUser':getUser})
    
    
    
@login_required(login_url="/admin-panel/")
def TicketCreate(request):
    if request.method == 'POST':
        usr = request.POST["user"]
        gid = request.POST["game"]      
        val = request.POST["val"]  
        win = request.POST["actv"] 
        py = request.POST["verificat"]  
        
        usr = Ticket(assign_to_id=usr, game_id=gid, value=val, is_winner=win, is_paid=py)
        usr.save()
        return redirect("/admin-panel/ticket-table/")
    else:
        getUser = User.objects.all()
        getGame = NewGame.objects.all()
        return render(request, "create-ticket.html", {'getUser':getUser,'getGame':getGame})
    
    
@login_required(login_url="/admin-panel/")   
def TicketTablePage(request):
    get_ticket = Ticket.objects.all()
    return render(request, "ticket-table.html", {'get_ticket':get_ticket})

@login_required(login_url="/admin-panel/")
def DeleteTicket(request, id):
    cty = Ticket.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/ticket-table/")


@login_required(login_url="/admin-panel/")
def EditTicket(request, id):
    if request.method == 'POST':
        usr = request.POST["user"]
        gid = request.POST["game"]      
        val = request.POST["val"]  
        win = request.POST["actv"] 
        py = request.POST["verificat"]   
        
          
        uplead = Ticket.objects.filter(id=id)        
        uplead.update(assign_to_id=usr, game_id=gid, value=val, is_winner=win, is_paid=py)
        messages.success(request, "Pay by wallet updated successfully")
        return redirect("/admin-panel/ticket-table/") 
    else:
        getTicket = Ticket.objects.get(id=id)    
        getUser = User.objects.all()
        getGame = NewGame.objects.all()
        return render(request, "edit-tickets.html", {'getTicket':getTicket, 'getUser':getUser, 'getGame':getGame})
    


@login_required(login_url="/admin-panel/")
def BuyTicketCreate(request):
    if request.method == 'POST':
        wa = request.POST["ticketid"]
        gn = request.POST["user"]
        ord_st = request.POST["actv"]
        pric = request.POST["order_price"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"]       
        
        
        usr = BuyTicket(ticketid_id=wa, userid_id=gn, order_status=ord_st, order_price=pric,razor_pay_order_id=rpoi,razor_pay_payment_id=tc,razor_pay_payment_signature=sa)
        usr.save()
        return redirect("/admin-panel/buy-ticket-table/")
    else:
        getTicket = Ticket.objects.all()
        getUser = User.objects.all()
        return render(request, "create-buy-ticket.html", {'getUser':getUser,'getTicket':getTicket})
    
    
@login_required(login_url="/admin-panel/")   
def BuyTicketTablePage(request):
    get_ticket = BuyTicket.objects.all()
    return render(request, "buy-ticket-table.html", {'get_ticket':get_ticket})

@login_required(login_url="/admin-panel/")
def DetailBuyTicket(request, id):
    get_ticket = BuyTicket.objects.get(id=id)
    return render(request, "buy-ticket-detail.html", {'get_ticket':get_ticket})

@login_required(login_url="/admin-panel/")
def DeleteBuyTicket(request, id):
    cty = BuyTicket.objects.get(id=id)
    cty.delete()
    return redirect("/admin-panel/buy-ticket-table/")


@login_required(login_url="/admin-panel/")
def EditBuyTicket(request, id):
    if request.method == 'POST':
        wa = request.POST["ticketid"]
        gn = request.POST["user"]
        ord_st = request.POST["actv"]
        pric = request.POST["order_price"]        
        rpoi = request.POST["razor_pay_order_id"]
        tc = request.POST["razor_pay_payment_id"]
        sa = request.POST["razor_pay_payment_signature"] 
        
          
        uplead = BuyTicket.objects.filter(id=id)        
        uplead.update(ticketid_id=wa, userid_id=gn, order_status=ord_st, order_price=pric,razor_pay_order_id=rpoi,razor_pay_payment_id=tc,razor_pay_payment_signature=sa)
        messages.success(request, "Wallet amount updated successfully")
        return redirect("/admin-panel/buy-ticket-table/") 
    else:
        getTicket = Ticket.objects.all()
        getBuy = BuyTicket.objects.get(id=id)    
        getUser = User.objects.all()
        return render(request, "edit-buy-ticket.html", {'getTicket':getTicket, 'getUser':getUser,'getBuy':getBuy})