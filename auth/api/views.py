from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.serialzier import UserRegistrationSerializer,UserLogin,UserProfileSerial
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated


#Creating tokens manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistration(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):

        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration success'},
            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLogin(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'logIn SuccessFul'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'Non_field_error':['Email or password is not valid']}}
                ,status=status.HTTP_404_NOT_FOUND)

class UserProfile(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]    
    def get(self,request,format=None):
        serialzier=UserProfileSerial(request.user)
        return Response(serialzier.data,status=status.HTTP_200_OK) 