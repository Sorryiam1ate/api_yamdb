from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import UsersViewSet, signup, token


router_v1 = SimpleRouter()
router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token),
    path(
        'token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    path('', include(router_v1.urls)),
]
