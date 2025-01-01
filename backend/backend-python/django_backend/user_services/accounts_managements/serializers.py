from rest_framework import serializers
from django.contrib.auth.models import User
from .models import InfoUser

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
    
class InfoUserSerializer(serializers.ModelSerializer):
    # Anda bisa menambahkan validasi untuk beberapa field jika diperlukan
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], required=False, allow_null=True)
    social_media_links = serializers.JSONField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], required=False, default='Active')

    class Meta:
        model = InfoUser
        fields = ['profile_picture', 'address', 'phone_number', 'date_of_birth', 'gender', 'social_media_links', 'status']
        
    def validate(self, data):
        # Bisa ditambahkan validasi kustom jika diperlukan
        return data