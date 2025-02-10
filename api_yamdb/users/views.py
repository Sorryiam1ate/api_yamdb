from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import AdminOnly, OnlyOwnAccountOrAdmins
from .serializers import (
    CustomUserSerializer,
    TokenSerializer,
    SignUpSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(
        username=request.data['username'],
        email=request.data['email'],
    ).exists():
        serializer.save()
    user = User.objects.get(
        username=request.data['username'],
        email=request.data['email']
    )
    conformation_code = default_token_generator.make_token(user)
    send_mail('Your confirmation code!',
              ('Ваш код подтверждения:\n' + conformation_code),
              settings.EMAIL_FOR_AUTH_LETTERS,
              [request.data['email']],
              fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = token = AccessToken.for_user(user)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(OnlyOwnAccountOrAdmins,),
        url_path='me'
    )
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user,
                                         data=request.data, partial=True)
        if serializer.is_valid():
            if 'role' in request.data:
                if user.role != 'user':
                    serializer.save(role=request.data['role'])
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.ValidationError('Получены неверные данные.')
