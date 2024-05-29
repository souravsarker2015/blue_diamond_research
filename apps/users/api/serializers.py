from rest_framework import serializers
from apps.users.models import User
from django.utils import timezone

from apps.users.utils import EmailAlreadyExistsException


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', "password", "password2"]

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        request = self.context.get('request')
        company_id = request.META.get('HTTP_COMPANY')

        if password != password2:
            raise serializers.ValidationError({'error': 'two password are not same'})
        if User.objects.filter(company_id=company_id, email=self.validated_data['email']).exists():
            raise EmailAlreadyExistsException()

        account = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company_id=company_id,
        )
        account.set_password(password)
        account.save()
        return account


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=555, write_only=True)
    uidb64 = serializers.CharField(max_length=555, write_only=True)

    def validate(self, attrs):
        password = attrs.get('new_password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Invalid token or User ID')

        except (TypeError, ValueError, OverflowError, User.DoesNotExist, DjangoUnicodeDecodeError):
            raise serializers.ValidationError('Invalid token or User ID')

        return {
            'user': user,
            'password': password
        }

    def create(self, validated_data):
        user = validated_data.get('user')
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user
