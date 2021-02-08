from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('posts/(?P<post_id>[0-9]+)/comments', CommentViewSet, basename='posts')


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
]