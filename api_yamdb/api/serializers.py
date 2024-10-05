from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.timezone import now

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


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category')

    def validate_year(self, value):
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError("Некорректная дата")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = (
            'pub_date',
            'review',
        )
