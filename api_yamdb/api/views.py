from rest_framework import viewsets

from api.serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
)

from reviews.models import Title, Category, Genre

from rest_framework import mixins


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
