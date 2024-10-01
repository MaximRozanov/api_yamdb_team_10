from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Titles, Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name')
        model = Category
        validators = [UniqueValidator, ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name')
        model = Genre
        validators = [UniqueValidator, ]