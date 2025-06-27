from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, CommentViewSet, UserViewSet


router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'users', UserViewSet, basename="users")


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]


