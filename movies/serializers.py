from rest_framework import serializers
from .models import Movie, Collection, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    class Meta:
        model = Movie
        fields = ['uuid', 'title', 'description', 'genres']

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            movie_uuid = str(movie_data.get('uuid'))
            movie, created = Movie.objects.get_or_create(uuid=movie_uuid, defaults=movie_data)
            collection.movies.add(movie)
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        if movies_data is not None:
            instance.movies.clear()
            for movie_data in movies_data:
                movie_uuid = str(movie_data.get('uuid'))
                movie, created = Movie.objects.get_or_create(uuid=movie_uuid, defaults=movie_data)
                instance.movies.add(movie)
        return super().update(instance, validated_data)

class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description']

class CollectionDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']
