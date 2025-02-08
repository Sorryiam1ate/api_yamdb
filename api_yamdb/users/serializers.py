from rest_framework import serializers
from .models import User
from .validators import validate_username
from django.core.validators import RegexValidator


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=(
                                         validate_username,
                                         RegexValidator(regex=r'^[\w.@+-]+\Z')
                                     ))

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if (
            not User.objects.filter(username=data.get('username')).exists()
            and User.objects.filter(email=data.get('email')).exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с такой почтой '
                'уже зарегестрирован')
        if (
            User.objects.filter(username=data.get('username')).exists()
            and not User.objects.filter(email=data.get('email')).exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем '
                'уже зарегестрирован')
        return data


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=(
                                         validate_username,
                                         RegexValidator(regex=r'^[\w.@+-]+\Z')
                                     ))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('username',)

    def validate(self, data):
        if (
            not User.objects.filter(username=data.get('username')).exists()
            and User.objects.filter(email=data.get('email')).exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с такой почтой '
                'уже зарегестрирован')
        if (
            User.objects.filter(username=data.get('username')).exists()
            and not User.objects.filter(email=data.get('email')).exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем '
                'уже зарегестрирован')
        return data
