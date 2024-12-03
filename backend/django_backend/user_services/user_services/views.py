from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        """
        Mengembalikan token JSON untuk user yang login menggunakan Google.
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(
                {
                    "token": response.data["access_token"],
                    "refresh_token": response.data["refresh_token"],
                    "user": response.data["user"],
                },
                status=status.HTTP_200_OK,
            )
        return response
