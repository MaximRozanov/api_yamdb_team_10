from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Titles, Genre, User, Review


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

    class Meta:
        fields = '__all__'
        model = Review


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Titles
        fields = '__all__'


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
        fields = '__all__'

    def validate_year(self, value):
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError("Некорректная дата")
        return value
