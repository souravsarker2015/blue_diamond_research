import requests

from .serializers import RegistrationSerializer, CustomLoginSerializer
from ..models import User
from oauth2_provider.views import TokenView
from django.contrib.auth import get_user_model
import dotenv

import json
import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import Application
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..usecases import UserDetailsUseCase
from ..utils import company_id_header_params

# dot env settings
dotenv.load_dotenv()


class CustomTokenView(TokenView):
    def validate_user(self, email, password, company_id):

        User = get_user_model()

        try:
            user = UserDetailsUseCase({'email': email, 'company_id': company_id}).execute()
            print('user')
            print(user)
        except User.DoesNotExist:
            return False

        if not user.check_password(password):
            return False

        if not user.is_active:
            return False
        return True

    def create_token_response(self, request):
        email = request.POST.get('username')
        password = request.POST.get('password')
        company_id = request.POST.get('company_id')

        if not self.validate_user(email, password, company_id):
            return self.error_response('Invalid user credentials')

        return super().create_token_response(request)


def get_access_token_from_refresh_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'client_id': os.environ.get('OAUTH2_PROVIDER_CLIENT_ID'),
        'client_secret': os.environ.get('OAUTH2_PROVIDER_CLIENT_SECRET'),
        'refresh_token': refresh_token
    }
    auth_service_url = os.environ.get('CUSTOM_AUTH_BACKEND_URL')
    auth_verify_url = f'{auth_service_url}o/token/'
    response = requests.post(auth_verify_url, data=data)
    response_data = response.json()
    return response_data


class RegistrationView(APIView, OAuthLibMixin):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @swagger_auto_schema(
        tags=["Login, Registration"],
        manual_parameters=company_id_header_params(),
        request_body=RegistrationSerializer
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data, context={'request': request})
        req_data = self.request.data
        print(req_data)
        if serializer.is_valid():
            user = serializer.save()
            company_id = request.META.get('HTTP_COMPANY', None)
            if not company_id:
                return Response({
                    "error": "Company Id is required for registration",
                    "status": 401
                })

            request.client = Application.objects.get(client_id=os.getenv('OAUTH2_PROVIDER_CLIENT_ID'))
            request.grant_type = 'password'

            request._request.POST = request._request.POST.copy()
            request._request.POST['username'] = req_data.get('email')
            request._request.POST['password'] = req_data.get('password')
            request._request.POST['client_id'] = os.getenv('OAUTH2_PROVIDER_CLIENT_ID')
            request._request.POST['client_secret'] = os.getenv('OAUTH2_PROVIDER_CLIENT_SECRET')
            request._request.POST['grant_type'] = 'password'

            url, headers, body, status_code = self.create_token_response(request._request)

            response_data = json.loads(body)

            response_data['status'] = status.HTTP_201_CREATED
            response_data['user'] = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            print(response_data)
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView, OAuthLibMixin):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @swagger_auto_schema(
        tags=["Login, Registration"],
        manual_parameters=company_id_header_params(),
        request_body=CustomLoginSerializer
    )
    def post(self, request, *args, **kwargs):
        print("request.data", request.data)
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            user = serializer.validated_data["username"]

            request.client = Application.objects.get(client_id=os.getenv('OAUTH2_PROVIDER_CLIENT_ID'))
            request.grant_type = 'password'
            request._request.POST = request._request.POST.copy()
            request._request.POST['username'] = serializer.validated_data['username']
            request._request.POST['password'] = serializer.validated_data['password']
            request._request.POST['client_id'] = os.getenv('OAUTH2_PROVIDER_CLIENT_ID')
            request._request.POST['client_secret'] = os.getenv('OAUTH2_PROVIDER_CLIENT_SECRET')
            request._request.POST['grant_type'] = 'password'

            url, headers, body, status_code = self.create_token_response(request)

            # Parse the body to a dictionary
            response_data = json.loads(body)

            # Add user information
            # response_data['user'] = {
            #     'email': user.email,
            #     'name': user.name
            # }

            return Response(response_data, status=status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView, OAuthLibMixin):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @swagger_auto_schema(
        tags=["Login, Registration"],
        manual_parameters=company_id_header_params(),
        request_body=CustomLoginSerializer
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            company_id = request.META.get('HTTP_COMPANY')
            if not company_id:
                return Response({
                    "error": "Company Id is required for registration",
                    "status": 401
                })

            user = User.objects.filter(company_id=company_id, email=username).first()
            print(user.email)
            if user:
                request.client = Application.objects.get(client_id=os.getenv('OAUTH2_PROVIDER_CLIENT_ID'))
                request.grant_type = 'password'
                request._request.POST = request._request.POST.copy()
                request._request.POST['username'] = serializer.validated_data['username']
                request._request.POST['password'] = serializer.validated_data['password']
                request._request.POST['client_id'] = os.getenv('OAUTH2_PROVIDER_CLIENT_ID')
                request._request.POST['client_secret'] = os.getenv('OAUTH2_PROVIDER_CLIENT_SECRET')
                request._request.POST['grant_type'] = 'password'

                url, headers, body, status_code = self.create_token_response(request._request)

                response_data = json.loads(body)
                return Response(response_data, status=status_code)

            else:
                data = {
                    'error': 'Invalid credentials',
                    'status': status.HTTP_401_UNAUTHORIZED
                }
                return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    @swagger_auto_schema(
        tags=["Login, Registration"],
        manual_parameters=company_id_header_params(),
        request_body=PasswordResetRequestSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        company_id = request.META.get('HTTP_COMPANY')
        user = User.objects.filter(email=email, company_id=company_id).first()

        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            reset_link = f'http://frontend.url/reset-password?uidb64={uidb64}&token={token}'

            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

        return Response({"message": "If the email is registered, you will receive a reset link."},
                        status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(
        tags=["Login, Registration"],
        request_body=PasswordResetSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
