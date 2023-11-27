from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import viewsets
from .models import *
from rest_framework.views import APIView
import razorpay
from tambola import settings

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
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
        return Response({'msg': 'Logout Successfully'},status=status.HTTP_200_OK)

class UserView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
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
            if len(request.FILES) !=0:
                if len(stu.profile_picture) > 0:
                    os.remove(stu.profile_picture.path)
                elif len(stu.profile_picture) == 0:
                    stu.profile_picture = request.FILES['profile_picture']
                    stu.save()
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors)

    def partial_update(self, request, pk):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = UserSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            if len(request.FILES) !=0:
                if len(stu.profile_picture) > 0:
                    os.remove(stu.profile_picture.path)
                elif len(stu.profile_picture) == 0:
                    stu.profile_picture = request.FILES['profile_picture']
                    stu.save()
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
        serializer = NewGameSerializer(data = request.data)  # form data conviert in json data
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

    def create(self, request):
        serializer = RuleInGameSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
            print(">>>>>>", client)
            payment = client.order.create({ 'amount': 100, 'currency': 'INR', 'payment_capture': 1})
            print("******************************")
            print(payment)
            print("******************************")
            return Response({'msg': 'Data Created','order_id':payment['id'],'user_id':serializer.data['user'],'status':serializer.data['walletstatus']}, status= status.HTTP_201_CREATED)
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
        print("request.data",request.data['amount'])
        prod = WalletAmt.objects.filter(user=request.data['user'])
        tik = BuyTicket.objects.filter(userid=request.data['user'])
        his = 0
        for j in tik:
            print("ticket", j)
            his += float(j.order_price)
        print("history", his)
        
        c = 0
        for i in prod:
            c = c + float(i.amount)
            print(i.amount)
        print("amount",c, request.data['amount'])
    
        uss=PayByWalletAmount.objects.filter(user=request.data['user']).exists()
        print('hcawdskj',uss)
        am = float(c)+float(request.data['amount'])-float(his)
        if uss:
            var2=PayByWalletAmount.objects.filter(user=request.data['user'])
            var2.update(amount=am)
        else:
            print(am)
            var1 = PayByWalletAmount(user_id=request.data['user'], amount=am)
            var1.save()
        if serializer.is_valid():
            serializer.save()
            print("====================",serializer.data['user'])
            
            
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
        serializer = BuyTicketSerializer(data = request.data)  # form data conviert in json data
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['userid'],"====")
            
            obj=WalletAmt.objects.filter(user=serializer.data['userid'])
            print("=========>>>>",obj)
            c = 0
            for i in obj:
                print(i)
                c = c + float(i.amount)
            print("c", c)    
                
            upl = PayByWalletAmount.objects.get(user=serializer.data['userid'])
            print("upl", upl)
            ll=upl.amount
            print('balance',ll)
            amtminus=c-float(serializer.data['order_price'])
            print("><><><><><>><>",amtminus,ll)
            uplead = PayByWalletAmount.objects.filter(user_id=serializer.data['userid'])
        
            uplead.update(amount=amtminus)
            
            print("===========Updated================")
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
    
    
class BuyTicketFilterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        print("user id: ",id)
        if User.objects.filter(id=id).exists():
            obj=BuyTicket.objects.filter(userid=id)
            createdserializer = BuyTicketSerializer(obj,many=True)

            return Response({'Created':createdserializer.data})
        else:
            raise AuthenticationFailed('Invalid ID, try again')
        
        
        
        

class GetWalletAmountView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        print("user id: ",id)
        if User.objects.filter(id=id).exists():
            obj=WalletAmt.objects.filter(user=id)
            print("=========>>>>",obj)
            c = 0
            for i in obj:
                print(i)
                c = c + float(i.amount)
                
            uss=PayByWalletAmount.objects.filter(user=id).exists()
            if uss:
                var2=PayByWalletAmount.objects.get(user=id)
                chg=var2.amount
            else:
                chg=0

            return Response({'Available Balance': c})
        else:
            raise AuthenticationFailed('Invalid ID, try again')




