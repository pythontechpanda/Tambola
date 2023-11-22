from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import viewsets
from .models import *


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

    # def create(self, request):
    #     serializer = NewGameSerializer(data = request.data)  # form data conviert in json data
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(serializer.data)
    #         return Response({'msg': 'Data Created'}, status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
