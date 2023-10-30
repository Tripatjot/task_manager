from rest_framework import serializers 
from .models import Users

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model =  Users
        fields = ('email', 'name', 'user_role')


    def create(self,validated_data):
        user = Users(
            name        = validated_data['name'],
            email       = validated_data['email'],
            user_role   = validated_data['user_role'],
        )
        password = '123456'
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

