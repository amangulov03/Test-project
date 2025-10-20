from rest_framework import serializers 
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import requests
from .models import LoginLog

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпали')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context['request']

        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        # Тестовое IP Адрес
        if ip_address in ('127.0.0.1', '::1', ''):
            ip_address = '103.106.3.0'

        # Определяем страну по IP
        country = 'Unknown'
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
            if response.status_code == 200:
                info = response.json()
                country = info.get('country', 'Unknown')
        except Exception as e:
            print('Ошибка при получении страны:', e)

        # Сохраняем лог
        LoginLog.objects.create(
            user=self.user,
            ip_address=ip_address,
            user_agent=user_agent,
            country=country
        )

        return data


class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = ['id', 'user', 'timestamp', 'ip_address', 'user_agent', 'country']
