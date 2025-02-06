from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import UsersViewSet, signup, token


urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token),
    path(
        'api/v1/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    # path('users', ),
    path('users/me/', UsersViewSet),
]
