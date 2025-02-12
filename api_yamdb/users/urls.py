from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet, signup, token

router_v1 = SimpleRouter()
router_v1.register(r'users', UsersViewSet, basename='users')

auth_patterns = [
    path('signup/', signup),
    path('token/', token),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_patterns), name='auth'),
]
