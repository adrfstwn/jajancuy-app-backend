from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterRequestSerializers(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirmation_password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        if data['password'] != data['confirmation_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        return data
    
class LoginRequestSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Email and Password are required!")
        
        user = User.objects.filter(email=email).first()
        
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid Credetials!")
        
        data['user'] =  user
        return data
    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
