from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Titles, Genre, User, Review, Comment


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')


class NoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        validators = [
            UniqueValidator,
        ]
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        validators = [
            UniqueValidator,
        ]
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = (
            'pub_date',
            'review',
        )
