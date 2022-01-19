from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    custom_token_obtain_pair, get_confirmation_code)

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

auth_patterns = [
    path('signup/', get_confirmation_code, name='signup'),
    path('token/', custom_token_obtain_pair, name='token_obtain_pair'),
]

v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_patterns)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
