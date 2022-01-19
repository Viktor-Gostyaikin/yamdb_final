from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from reviews.models import Category, Genre, Review, Title
from .filter import TitleFilter
from .mixins import ListOrCreateOrDestroy
from .permissions import (AdminOnly, AuthorOrAdminOrModeratorOnly,
                          ReadOrAdminOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleSerializer, UserMeSerializer,
                          UserRegistrationSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    '''
    Предоставляет возможность работать объектами пользователей:
    читать, создавать, редактировать, удалять.
    Базовый доступ - только для админитратора.
    Действие 'me/' доступно для всех авторизованых пользователей,
    где доступно получить или изменить свои данные.
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ['username']
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(
        methods=['get', 'put', 'patch', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class Custom_TokenObtainPairView(TokenViewBase):
    ''' Получение JWT-токена в обмен на username и confirmation code. '''
    serializer_class = GetTokenSerializer


custom_token_obtain_pair = Custom_TokenObtainPairView.as_view()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    '''
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    '''
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    _user = User.objects.create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
    )
    confirmation_code = _user.make_confirmation_code()
    _user.set_confirmation_code(confirmation_code=confirmation_code)
    _user.save()
    _user.email_user(
        subject='Создан confirmation code для получения token',
        message=f'Ваш confirmation code {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CategoryViewSet(ListOrCreateOrDestroy):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminOnly,)


class GenreViewSet(ListOrCreateOrDestroy):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['category', 'genre', 'name', 'year']
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    permission_classes = (ReadOrAdminOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    '''
    Предоставляет возможность работать с отзывами к произведениям:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ.
    '''

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrAdminOrModeratorOnly,
                          permissions.IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=get_object_or_404(
                Title, id=self.kwargs['title_id']
            )
        )


class CommentViewSet(viewsets.ModelViewSet):

    '''
    Предоставляет возможность работать с комментариями к отзывам:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ по ролям.
    '''

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrAdminOrModeratorOnly,
                          permissions.IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title=self.kwargs['title_id'],)
        serializer.save(author=self.request.user, review=review)
