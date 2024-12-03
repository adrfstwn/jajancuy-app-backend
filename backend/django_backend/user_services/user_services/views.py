from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class RegisterAPIView(APIView):
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
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
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

        # Verifikasi password
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
   
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        
        # Panggil login Google bawaan
        super().post(request, *args, **kwargs)

        user = self.user
        
        # Buat JWT token internal
        refresh = RefreshToken.for_user(user)

        return Response({
             'user_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)