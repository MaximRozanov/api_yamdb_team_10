from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Titles, Genre, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role')


class NoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role')
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


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
