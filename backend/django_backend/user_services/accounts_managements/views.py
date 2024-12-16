from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from .models import Role, UserRole
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_role_to_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        role_admin = Role.objects.get(name="Admin")
        if not UserRole.objects.filter(user_id=instance.id, role=role_admin).exists():
            UserRole.objects.create(user_id=instance.id, role=role_admin)
            
class Register(APIView):
    def post(self, request):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        confirmation_password = data.get('confirmation_password')

        if not first_name or not last_name or not email or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != confirmation_password:
            return Response({'error': 'Password doesn\'t match'}, status=status.HTTP_400_BAD_REQUEST)

        username = email.split('@')[0]
        
        user = User.objects.create_user(
            first_name=first_name, 
            last_name=last_name, 
            username=username, 
            email=email, 
            password=password
        )
       
        role_user = Role.objects.get(name="User")
        UserRole.objects.create(user_id=user.id, role=role_user)

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class Login(APIView):
    def post(self, request):
        data = request.data
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        if not username_or_email or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if '@' in username_or_email:
            # Jika mengandung '@', anggap itu email
            user = User.objects.filter(email=username_or_email).first()
        else:
            # Jika tidak mengandung '@', anggap itu username
            user = User.objects.filter(username=username_or_email).first()
            
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        
        user_roles = UserRole.objects.filter(user_id=user.id).select_related('role').first()
        roles = user_roles.role.name
        
        # user_roles = UserRole.objects.filter(user_id=user.id).select_related('role')
        # roles = [user_object.role.name for user_object in user_roles]

        return Response({
            'user_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': roles,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
   
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        
        # Panggil login Google bawaan
        super().post(request, *args, **kwargs)

        user = self.user
        
        role_user = Role.objects.get(name="User")
        if not UserRole.objects.filter(user_id=user.id, role=role_user).exists():
            UserRole.objects.create(user_id=user.id, role=role_user)
        
        refresh = RefreshToken.for_user(user)

        user_roles = UserRole.objects.filter(user_id=user.id).select_related('role').first()
        roles = user_roles.role.name 
        
        return Response({
             'user_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': roles,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
        
class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Construct password reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            subject='Password Reset Request',
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
    
class ResetPassword(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get('password')
        confirmation_password = request.data.get('confirmation_password')

        if not password or not confirmation_password:
            return Response({'error': 'Password and confirmation password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirmation_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

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
    
# class EditPassword(APIView):
    