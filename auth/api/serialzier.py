from rest_framework import serializers
from api. models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['name','email','password','password2','roll']
        extra_kwargs={
            'password':{'write_only':True}
        }

#Validating Password and confirm Password while Registration

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match ")
        return attrs
        
    def create(self,validate_Data):
        return User.objects.create_user(**validate_Data) 


class UserLogin(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=100)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerial(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','email','name']