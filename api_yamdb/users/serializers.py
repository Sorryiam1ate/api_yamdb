from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.constants import (
    EMAIL_MAX_LENGTH,
    PATTERN_USERNAME,
    USERNAME_MAX_LENGTH
)

from .models import User
from .validators import validate_username


def validate_username_and_email(data):
    username = User.objects.filter(username=data.get('username')).exists()
    email = User.objects.filter(email=data.get('email')).exists()
    if not username and email:
        raise serializers.ValidationError(
            'Пользователь с такой почтой '
            'уже зарегестрирован')
    if username and not email:
        raise serializers.ValidationError(
            'Пользователь с таким именем '
            'уже зарегестрирован')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        allow_blank=False
    )
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        allow_blank=False,
        validators=(
            validate_username,
            RegexValidator(regex=PATTERN_USERNAME),
        ))

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = (validate_username_and_email,)

    def create(self, data):
        user, _ = User.objects.get_or_create(
            username=data['username'],
            email=data['email']
        )
        return user


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        allow_blank=False
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        get_object_or_404(User, username=data.get('username'))
        if not default_token_generator.check_token(
            data.get('username'),
            data.get('confirmation_code')
        ):
            raise serializers.ValidationError('Неверный данные')
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        allow_blank=False
    )
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        allow_blank=False,
        validators=(
            validate_username,
            RegexValidator(regex=PATTERN_USERNAME),
        ))

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('username',)
        validators = (validate_username_and_email,)
