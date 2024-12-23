from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterRequestSerializers(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
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
    
class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email doesn't exist!")
        return email

class ResetPasswordRequestSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Password do not match!")
        return data