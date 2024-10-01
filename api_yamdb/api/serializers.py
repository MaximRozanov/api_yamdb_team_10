from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Titles, Genre, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'name'
        model = Category
        validators = [
            UniqueValidator,
        ]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'name'
        model = Genre
        validators = [
            UniqueValidator,
        ]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Review
