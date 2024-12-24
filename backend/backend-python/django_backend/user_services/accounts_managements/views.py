from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Role, UserRole
from .serializers import (LoginRequestSerializers, RegisterRequestSerializers, 
                          ForgotPasswordRequestSerializer, ResetPasswordRequestSerializer)
        
@receiver(post_save, sender=User)
def assign_role_to_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        role_admin = Role.objects.get(name="Admin")
        if not UserRole.objects.filter(user=instance, role=role_admin).exists():
            UserRole.objects.create(user=instance, role=role_admin)
            
def assign_default_role(user):
    role, _ = Role.objects.get_or_create(name="User")
    UserRole.objects.get_or_create(user=user, role=role)
    
def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'TokenAccess': str(refresh.access_token),
        'TokenRefresh': str(refresh),
    }

def send_reset_email(user, email):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
    send_mail(
        subject='Password Reset Request',
        message=f"Click the link below to reset your password:\n{reset_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
            
class Register(APIView):
    def post(self, request):
        serializerRegister = RegisterRequestSerializers(data=request.data)
        
        serializerRegister.is_valid(raise_exception=True)
        
        data = serializerRegister.validated_data
        
        # create username from email
        usernameFromEmail = data['email'].split('@')[0]
        
        # create to db
        user = User.objects.create_user(
            first_name=data['first_name'], 
            last_name=data['last_name'], 
            username=usernameFromEmail, 
            email=data['email'], 
            password=data['password']
        )
        assign_default_role(user)
        
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    
class Login(APIView):
    def post(self, request):
        serializerLogin = LoginRequestSerializers(data=request.data)
        serializerLogin.is_valid(raise_exception=True)
        
        user = serializerLogin.validated_data['user']
        
        roles = user.userrole_set.first().role.name if user.userrole_set.exists() else "No role assigned"
            
        # Generate JWT Token
        tokens = generate_jwt_tokens(user)

        return Response({
            'message': 'User loged in successfully',
            'user_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': roles,
            },
            **tokens,
        }, status=status.HTTP_200_OK)
   
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):

        # # Panggil login Google bawaan
        super().post(request, *args, **kwargs)
        user = self.user

        time_difference = (user.last_login - user.date_joined)
        
        if time_difference < timedelta(seconds=5):
            response_message = "User registered successfully"
        else:
            response_message = "User logged in successfully"
        
        # Ensure the user has a role (Assign default role if not assigned)
        if not UserRole.objects.filter(user=user).exists():
            assign_default_role(user)
            
        tokens = generate_jwt_tokens(user)
        roles = user.userrole_set.first().role.name if user.userrole_set.exists() else "No role assigned"
        
        return Response({
            'message': response_message,
            'user_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': roles,
            },
            **tokens,
        }, status=status.HTTP_200_OK)
        
class ForgotPassword(APIView):
    def post(self, request):
        forgotPasswordSerializer = ForgotPasswordRequestSerializer(data=request.data)
        
        forgotPasswordSerializer.is_valid(raise_exception=True)
        
        email = forgotPasswordSerializer.validated_data['email']
        
        user = User.objects.filter(email=email).first()
        
        send_reset_email(user, email)
        
        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
    
class ResetPassword(APIView):
    def post(self, request, uidb64, token):
        resetPasswordSerializer = ResetPasswordRequestSerializer(data=request.data)
        
        resetPasswordSerializer.is_valid(raise_exception=True)
        password = resetPasswordSerializer.validated_data['password']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValidationError):
            return Response({'error': 'Invalid token or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user password
        user.set_password(password)
        user.save()
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    
    