from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import viewsets
from .models import *
from rest_framework.views import APIView
from datetime import datetime
import pytz


# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        if user_data['refer_code'] != 0:
            refer_user=User.objects.get(my_code=user_data['refer_code'])
            refer_by_user_update=User.objects.filter(id=user_data['id'])
            refer_by_user_update.update(refer_by=refer_user.username)
            user_wallet=WalletAdd(user_id=refer_user.id,walletamount=5,walletstatus=True)
            user_wallet.save()
            user_walletAmt=WalletAmt(walt_id = user_wallet.id,user_id = refer_user.id,payment_status = True,
                                     amount = 5,razor_pay_order_id = 'Refer',
                                     razor_pay_payment_id = 'Refer',razor_pay_payment_signature = 'Refer')
            user_walletAmt.save()
            prod = WalletAmt.objects.filter(user=refer_user.id)
            tik = BuyTicket.objects.filter(userid=refer_user.id)
            withdr = WithdrawRequest.objects.Filter(user=refer_user.id,is_completed=True)
            his = 0
            for j in tik:
                his += float(j.order_price)
            c = 0
            for i in prod:
                c = c + float(i.amount)
            w=0
            for k in withdr:
                w = w + float(k.amount)
            uss=PayByWalletAmount.objects.filter(user=refer_user.id).exists()
            am = float(c)-float(his)-float(w)
            if uss:
                var2=PayByWalletAmount.objects.filter(user=refer_user.id)
                var2.update(amount=am)
            else:
                print(am)
                var1 = PayByWalletAmount(user_id=refer_user.id, amount=am)
                var1.save()
        else:
            pass


        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

class UserView(viewsets.ViewSet):
    def list(self, request):      # list - get all record
        stu = User.objects.all()
        serializer = UserSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = User.objects.get(id=id)
            serializer = UserSerializer(stu)
            return Response(serializer.data)

    # def create(self, request):
    #     serializer = UserSerializer(data = request.data)  # form data conviert in json data
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(serializer.data)
    #         return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = UserSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = UserSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
class CityView(viewsets.ViewSet):
    def list(self, request):      # list - get all record
        stu = City.objects.all()
        serializer = CitySerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = City.objects.get(id=id)
            serializer = CitySerializer(stu)
            return Response(serializer.data)

    # def create(self, request):
    #     serializer = CitySerializer(data = request.data)  # form data conviert in json data
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(serializer.data)
    #         return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = City.objects.get(pk=id)
        serializer = CitySerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = City.objects.get(pk=id)
        serializer = CitySerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = City.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})


class Game_RuleView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Game_Rule.objects.all()
        serializer = Game_RuleSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Game_Rule.objects.get(id=id)
            serializer = Game_RuleSerializer(stu)
            return Response(serializer.data)

    # def create(self, request):
    #     serializer = Game_RuleSerializer(data = request.data)  # form data conviert in json data
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(serializer.data)
    #         return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Game_Rule.objects.get(pk=id)
        serializer = Game_RuleSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Game_Rule.objects.get(pk=id)
        serializer = Game_RuleSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Game_Rule.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

class NewGameView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = NewGame.objects.all()
        serializer = NewGameSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = NewGame.objects.get(id=id)
            serializer = NewGameSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = NewGamePostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['number_of_tickets'])
            for tick in range(int(serializer.data['number_of_tickets'])):
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

                tk=Ticket(game_id=serializer.data['id'],assign_to_id=1,value=rw)
                tk.save()
                user_referal=User.objects.get(id=serializer.data['user'])
                print('>>>>>>>>>',user_referal.refer_code)
                if user_referal.refer_code != 0:
                    refer_user=User.objects.get(my_code=user_referal.refer_code)
                    user_wallet=WalletAdd(user_id=refer_user.id,walletamount=1,walletstatus=True)
                    user_wallet.save()
                    user_walletAmt=WalletAmt(walt_id = user_wallet.id,user_id = refer_user.id,payment_status = True,
                                            amount = 1,razor_pay_order_id = 'Refer',
                                            razor_pay_payment_id = 'Refer',razor_pay_payment_signature = 'Refer')
                    user_walletAmt.save()
                    prod = WalletAmt.objects.filter(user=refer_user.id)
                    tik = BuyTicket.objects.filter(userid=refer_user.id)
                    withdr = WithdrawRequest.objects.Filter(user=refer_user.id,is_completed=True)
                    his = 0
                    for j in tik:
                        his += float(j.order_price)
                    c = 0
                    for i in prod:
                        c = c + float(i.amount)
                    w=0
                    for k in withdr:
                        w = w + float(k.amount)
                    uss=PayByWalletAmount.objects.filter(user=refer_user.id).exists()
                    am = float(c)-float(his)-float(w)
                    if uss:
                        var2=PayByWalletAmount.objects.filter(user=refer_user.id)
                        var2.update(amount=am)
                    else:
                        print(am)
                        var1 = PayByWalletAmount(user_id=refer_user.id, amount=am)
                        var1.save()
                else:
                    pass
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = NewGame.objects.get(pk=id)
        serializer = NewGameSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = NewGame.objects.get(pk=id)
        serializer = NewGameSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = NewGame.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

class AssignToFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        print('uid',id)
        if Ticket.objects.filter(game_id=id).exists():
            obj=Ticket.objects.filter(game_id=id)
            ticket_list=[]
            for i in obj:
                if i.assign_to_id==1:
                    pass
                else:
                    ticket_list.append(i)
            serializer = TicketSerializer(ticket_list,many=True)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        # return Response('uid,id')

    
class RuleInGameView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = RuleInGame.objects.all()
        serializer = RuleInGameSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = RuleInGame.objects.get(id=id)
            serializer = RuleInGameSerializer(stu)
            return Response(serializer.data)

    # def create(self, request):
    #     serializer = RuleInGameSerializer(data = request.data)  # form data conviert in json data
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(serializer.data)
    #         return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = RuleInGame.objects.get(pk=id)
        serializer = RuleInGameSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = RuleInGame.objects.get(pk=id)
        serializer = RuleInGameSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = RuleInGame.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
class RuleInGameFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):

        if RuleInGame.objects.filter(game_id=id).exists():
            obj=RuleInGame.objects.filter(game_id=id)
            serializer = RuleInGameSerializer(obj,many=True)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Invalid credentials, try again')

class HelpAndSupportView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = HelpAndSupport.objects.all()
        serializer = HelpAndSupportSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = HelpAndSupport.objects.get(id=id)
            serializer = HelpAndSupportSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = HelpAndSupportSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = HelpAndSupport.objects.get(pk=id)
        serializer = HelpAndSupportSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = HelpAndSupport.objects.get(pk=id)
        serializer = HelpAndSupportSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = HelpAndSupport.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

class PageView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,uid):
        print('uid',uid)
        uid_main=uid.replace('_', ' ')
        if Page.objects.filter(title=uid_main).exists():
            obj=Page.objects.filter(title=uid_main)
            serializer = PageSerializer(obj,many=True)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Invalid credentials, try again')

    
class AddMoneyView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = AddMoney.objects.all()
        serializer = AddMoneySerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = AddMoney.objects.get(id=id)
            serializer = AddMoneySerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = AddMoneySerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = AddMoney.objects.get(pk=id)
        serializer = AddMoneySerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = AddMoney.objects.get(pk=id)
        serializer = AddMoneySerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = AddMoney.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})


    
class WalletAddView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = WalletAdd.objects.all()
        serializer = WalletAddSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = WalletAdd.objects.get(id=id)
            serializer = WalletAddSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = WalletAddSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = WalletAdd.objects.get(pk=id)
        serializer = WalletAddSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = WalletAdd.objects.get(pk=id)
        serializer = WalletAddSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = WalletAdd.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
   
class WalletAmtView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = WalletAmt.objects.all()
        serializer = WalletAmtSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = WalletAmt.objects.get(id=id)
            serializer = WalletAmtSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = WalletAmtSerializer(data = request.data)  # form data conviert in json data
        prod = WalletAmt.objects.filter(user=request.data['user'])
        tik = BuyTicket.objects.filter(userid=request.data['user'])
        withdr = WithdrawRequest.objects.Filter(user=request.data['user'])
        his = 0
        for j in tik:
            his += float(j.order_price)
        c = 0
        for i in prod:
            c = c + float(i.amount)
        w=0
        for k in withdr:
            w = w + float(k.amount)
        uss=PayByWalletAmount.objects.filter(user=request.data['user']).exists()
        am = float(c)+float(request.data['amount'])-float(his)-float(w)
        if uss:
            var2=PayByWalletAmount.objects.filter(user=request.data['user'])
            var2.update(amount=am)
        else:
            print(am)
            var1 = PayByWalletAmount(user_id=request.data['user'], amount=am)
            var1.save()
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = WalletAmt.objects.get(pk=id)
        serializer = WalletAmtSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = WalletAmt.objects.get(pk=id)
        serializer = WalletAmtSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = WalletAmt.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
  
class PayByWalletAmountView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = PayByWalletAmount.objects.all()
        serializer = PayByWalletAmountSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = PayByWalletAmount.objects.get(id=id)
            serializer = PayByWalletAmountSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = PayByWalletAmountSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = PayByWalletAmount.objects.get(pk=id)
        serializer = PayByWalletAmountSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = PayByWalletAmount.objects.get(pk=id)
        serializer = PayByWalletAmountSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = PayByWalletAmount.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

class JoinAGameFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = request.data
        if NewGame.objects.filter(private_code=data['game_code']).exists():
            join_game=NewGame.objects.filter(private_code=data['game_code'])
            serializer = NewGameSerializer(join_game,many=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            raise AuthenticationFailed('Invalid Code, try again')
 

class HomeFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        current_dateTime = datetime.now()
        if User.objects.filter(id=id).exists():
            obj=NewGame.objects.all()
            upcoming=[]
            utc=pytz.UTC
            for i in obj:
                upcomingdetail={}
                start_time = current_dateTime.replace(tzinfo=utc)
                end_time =i.start_at.replace(tzinfo=utc)
                if end_time > start_time:
                    objcount=NewGame.objects.filter(user_id=i.user.id).count()

                    played_ticket=Ticket.objects.filter(assign_to_id=i.user.id)
                    played=[]
                    for j in played_ticket:
                        if j.game in played:
                            pass
                        else:
                            played.append(j.game)
                   
                    upcomingdetail.update({'game_id':i.id,
                                           'game_name':i.game_name,
                                           'message_for_player':i.message_for_player,
                                           'lobby':i.lobby,
                                           'ticket_cost':i.ticket_cost,
                                           'start_at':i.start_at,
                                           'ticket_request_till':i.ticket_request_till,
                                           'number_of_ticket':i.number_of_tickets,
                                           'timer':i.timer,
                                           'private_code':i.private_code,
                                        #    'game_counter':i.game_counter,
                                           'is_completed':i.is_completed,
                                        #    'created_at':i.created_at,
                                           'user_id': i.user.id,
                                            'first_name': i.user.first_name,
                                            'username': i.user.username,
                                            'profile_picture':i.user.profile_picture,
                                            'city':i.user.city.city_name,
                                            'gender':i.user.gender,
                                            'date_of_birth':i.user.date_of_birth,
                                            'mobile_no':i.user.mobile_no,
                                            'is_verified':i.user.is_verified,
                                            'is_above18':i.user.is_above18,
                                            'refer_code':i.user.refer_code,
                                            'refer_by':i.user.refer_by,
                                            'my_code':i.user.my_code,
                                            'played':len(played),
                                            'created':objcount})
                    upcoming.append(upcomingdetail)
            print('upcoming',upcoming)
            up= UpcomingSerializer(upcoming,many=True)

            live=[]
            for k in obj:
                livedetail={}
                start_time = current_dateTime.replace(tzinfo=utc)
                end_time =k.start_at.replace(tzinfo=utc)
                if end_time < start_time and k.is_completed==False:                   
                    # live.append(k)
                    obj=NewGame.objects.filter(user_id=k.user.id).count()

                    played_ticket=Ticket.objects.filter(assign_to_id=k.user.id)
                    played=[]
                    for j in played_ticket:
                        if j.game in played:
                            pass
                        else:
                            played.append(j.game)
                   
                    livedetail.update({'game_id':k.id,
                                           'game_name':k.game_name,
                                           'message_for_player':k.message_for_player,
                                           'lobby':k.lobby,
                                           'ticket_cost':k.ticket_cost,
                                           'start_at':k.start_at,
                                           'ticket_request_till':k.ticket_request_till,
                                           'number_of_ticket':k.number_of_tickets,
                                           'timer':k.timer,
                                           'private_code':k.private_code,
                                        #    'game_counter':k.game_counter,
                                           'is_completed':k.is_completed,
                                        #    'created_at':k.created_at,
                                           'user_id': k.user.id,
                                            'first_name': k.user.first_name,
                                            'username': k.user.username,
                                            'profile_picture':k.user.profile_picture,
                                            'city':k.user.city.city_name,
                                            'gender':k.user.gender,
                                            'date_of_birth':k.user.date_of_birth,
                                            'mobile_no':k.user.mobile_no,
                                            'is_verified':k.user.is_verified,
                                            'is_above18':k.user.is_above18,
                                            'refer_code':k.user.refer_code,
                                            'refer_by':k.user.refer_by,
                                            'my_code':k.user.my_code,
                                            'played':len(played),
                                            'created':obj})
                    live.append(livedetail)
            liveserializer = LiveSerializer(live,many=True)

            return Response({'Upcoming':up.data,'Live':liveserializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        
# class HomeFilterView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     def get(self,request,id):
#         current_dateTime = datetime.now()
#         if User.objects.filter(id=id).exists():
#             obj=NewGame.objects.all()
#             upcoming=[]
#             utc=pytz.UTC
#             for i in obj:
#                 start_time = current_dateTime.replace(tzinfo=utc)
#                 end_time =i.start_at.replace(tzinfo=utc)
#                 if end_time > start_time:
#                     upcoming.append(i)
#             upcomingserializer = NewGameSerializer(upcoming,many=True)

#             live=[]
#             for i in obj:
#                 start_time = current_dateTime.replace(tzinfo=utc)
#                 end_time =i.start_at.replace(tzinfo=utc)
#                 if end_time <= start_time and i.is_completed==False:                   
#                     live.append(i)
#             liveserializer = NewGameSerializer(live,many=True)

#             return Response({'Live':liveserializer.data,'Upcoming':upcomingserializer.data})
#         else:
#             raise AuthenticationFailed('Invalid ID, try again')

class MyGameFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        if User.objects.filter(id=id).exists():
            obj=NewGame.objects.filter(user_id=id)
            c=[]
            for h in obj:
                createddetail={}
            
                objcount=NewGame.objects.filter(user_id=h.user.id).count()

                played_ticket=Ticket.objects.filter(assign_to_id=h.user.id)
                played=[]
                for j in played_ticket:
                    if j.game in played:
                        pass
                    else:
                        played.append(j.game)
                
                createddetail.update({'game_id':h.id,
                                        'game_name':h.game_name,
                                        'message_for_player':h.message_for_player,
                                        'lobby':h.lobby,
                                        'ticket_cost':h.ticket_cost,
                                        'start_at':h.start_at,
                                        'ticket_request_till':h.ticket_request_till,
                                        'number_of_ticket':h.number_of_tickets,
                                        'timer':h.timer,
                                        'private_code':h.private_code,
                                    #    'game_counter':h.game_counter,
                                        'is_completed':h.is_completed,
                                    #    'created_at':h.created_at,
                                        'user_id': h.user.id,
                                        'first_name': h.user.first_name,
                                        'username': h.user.username,
                                        'profile_picture':h.user.profile_picture,
                                        'city':h.user.city.city_name,
                                        'gender':h.user.gender,
                                        'date_of_birth':h.user.date_of_birth,
                                        'mobile_no':h.user.mobile_no,
                                        'is_verified':h.user.is_verified,
                                        'is_above18':h.user.is_above18,
                                        'refer_code':h.user.refer_code,
                                        'refer_by':h.user.refer_by,
                                        'my_code':h.user.my_code,
                                        'played':len(played),
                                        'created':objcount})
                c.append(createddetail)
            createdserializer = CreatedSerializer(c,many=True)

            played_ticket=Ticket.objects.filter(assign_to=id)
            played=[]
            for i in played_ticket:
                playeddetail={}
            
                objcount=NewGame.objects.filter(user_id=i.game.user.id).count()

                played_ticket1=Ticket.objects.filter(assign_to_id=i.game.user.id)
                played1=[]
                for j in played_ticket1:
                    if j.game in played1:
                        pass
                    else:
                        played1.append(j.game)
                
                playeddetail.update({'game_id':i.game.id,
                                        'game_name':i.game.game_name,
                                        'message_for_player':i.game.message_for_player,
                                        'lobby':i.game.lobby,
                                        'ticket_cost':i.game.ticket_cost,
                                        'start_at':i.game.start_at,
                                        'ticket_request_till':i.game.ticket_request_till,
                                        'number_of_ticket':i.game.number_of_tickets,
                                        'timer':i.game.timer,
                                        'private_code':i.game.private_code,
                                    #    'game_counter':i.game.game_counter,
                                        'is_completed':i.game.is_completed,
                                    #    'created_at':i.game.created_at,
                                        'user_id': i.game.user.id,
                                        'first_name': i.game.user.first_name,
                                        'username': i.game.user.username,
                                        'profile_picture':i.game.user.profile_picture,
                                        'city':i.game.user.city.city_name,
                                        'gender':i.game.user.gender,
                                        'date_of_birth':i.game.user.date_of_birth,
                                        'mobile_no':i.game.user.mobile_no,
                                        'is_verified':i.game.user.is_verified,
                                        'is_above18':i.game.user.is_above18,
                                        'refer_code':i.game.user.refer_code,
                                        'refer_by':i.game.user.refer_by,
                                        'my_code':i.game.user.my_code,
                                        'played':len(played),
                                        'created':objcount})

                played.append(playeddetail)
            playedserializer = PlayedSerializer(played,many=True)

            return Response({'Created':createdserializer.data,'Played':playedserializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        
   
class ComplimentView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Compliment.objects.all()
        serializer = ComplimentSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Compliment.objects.get(id=id)
            serializer = ComplimentSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = ComplimentPostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Compliment.objects.get(pk=id)
        serializer = ComplimentSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Compliment.objects.get(pk=id)
        serializer = ComplimentSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Compliment.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

class ComplimentFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        if User.objects.filter(id=id).exists():
            obj=Compliment.objects.filter(compliment_to_id=id)
            serializer = ComplimentSerializer(obj,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed('Invalid ID, try again')

   
class TicketView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Ticket.objects.all()
        serializer = TicketSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Ticket.objects.get(id=id)
            serializer = TicketSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = TicketPostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Ticket.objects.get(pk=id)
        serializer = TicketSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Ticket.objects.get(pk=id)
        serializer = TicketSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Ticket.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

   
class ClaimRuleView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = ClaimRule.objects.all()
        serializer = ClaimRuleSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = ClaimRule.objects.get(id=id)
            serializer = ClaimRuleSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = ClaimRulePostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = ClaimRule.objects.get(pk=id)
        serializer = ClaimRuleSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = ClaimRule.objects.get(pk=id)
        serializer = ClaimRuleSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = ClaimRule.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

class NotificationView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = Notification.objects.all()
        serializer = NotificationSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Notification.objects.get(id=id)
            serializer = NotificationSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = NotificationPostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Notification.objects.get(pk=id)
        serializer = NotificationSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = Notification.objects.get(pk=id)
        serializer = NotificationSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = Notification.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
class WithdrawRequestView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = WithdrawRequest.objects.all()
        serializer = WithdrawRequestSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = WithdrawRequest.objects.get(id=id)
            serializer = WithdrawRequestSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = WithdrawRequestPostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            if BankDetail.objects.filter(user_id=serializer.data['id']).exists():
                return Response({'msg': 'Data Created','id':serializer.data['id'],'Bank_Details':'Exist'}, status= status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Data Created','id':serializer.data['id'],'Bank_Details':'Not Exist'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = WithdrawRequest.objects.get(pk=id)
        serializer = WithdrawRequestSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = WithdrawRequest.objects.get(pk=id)
        serializer = WithdrawRequestSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = WithdrawRequest.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
    
class BankDetailView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = BankDetail.objects.all()
        serializer = BankDetailSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = BankDetail.objects.get(id=id)
            serializer = BankDetailSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = BankDetailPostSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','id':serializer.data['id']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = BankDetail.objects.get(pk=id)
        serializer = BankDetailSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = BankDetail.objects.get(pk=id)
        serializer = BankDetailSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = BankDetail.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})
    
class NotificationFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        if User.objects.filter(id=id).exists():
            obj=Notification.objects.filter(user_id=id)
            serializer = NotificationSerializer(obj,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed('Invalid ID, try again') 
        
class TicketFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        if NewGame.objects.filter(id=id).exists():
            obj=Ticket.objects.filter(game_id=id)
            serializer = TicketSerializer(obj,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        

class BuyTicketView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):      # list - get all record
        stu = BuyTicket.objects.all()
        serializer = BuyTicketSerializer(stu, many=True)    # many use for bulk data come 
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = BuyTicket.objects.get(id=id)
            serializer = BuyTicketSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = BuyTicketPostSerializer(data = request.data)  # form data conviert in json data
        prod = WalletAmt.objects.filter(user=request.data['user'])
        tik = BuyTicket.objects.filter(userid=request.data['user'])
        withdr = WithdrawRequest.objects.Filter(user=request.data['user'])
        his = 0
        for j in tik:
            his += float(j.order_price)
        c = 0
        for i in prod:
            c = c + float(i.amount)
        w=0
        for k in withdr:
            w = w + float(k.amount)
        uss=PayByWalletAmount.objects.filter(user=request.data['user']).exists()
        am = float(c)+float(request.data['order_price'])-float(his)-float(w)
        if uss:
            var2=PayByWalletAmount.objects.filter(user=request.data['user'])
            var2.update(amount=am)
        else:
            print(am)
            var1 = PayByWalletAmount(user_id=request.data['user'], amount=am)
            var1.save()
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','ticket_id':serializer.data['ticketid'],'user_id':serializer.data['userid']}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        id = pk
        stu = BuyTicket.objects.get(pk=id)
        serializer = BuyTicketSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = BuyTicket.objects.get(pk=id)
        serializer = BuyTicketSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Update'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        stu = BuyTicket.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})

