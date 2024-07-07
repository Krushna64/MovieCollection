from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Movie, Collection
from .serializers import RegisterSerializer, MovieSerializer, CollectionSerializer, CollectionListSerializer, CollectionDetailSerializer
from .services import MovieAPIService
from rest_framework.views import APIView
from .middleware import RequestCounterMiddleware
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from collections import Counter


# Create your views here.

class RegisterView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class MovieView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            service = MovieAPIService()
            page = request.query_params.get('page', 1)
            data = service.fetch_movies(page=page)
            if not data:
                return Response("Failed to fetch movies", status=status.HTTP_503_SERVICE_UNAVAILABLE)
            serializer = MovieSerializer(data['results'], many=True)    # since we get results key and not data key
            response_data = {
                "count": data['count'],
                "next": data['next'],
                "previous": data['previous'],
                "data": serializer.data # Here we get key "results" but we wanna display key "data" as per requirement
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class CollectionView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, uuid=None):
        try:
            if uuid:
                collection = Collection.objects.get(uuid=uuid, user=request.user)
                serializer = CollectionDetailSerializer(collection)
                return Response(serializer.data)
            else:
                collections = Collection.objects.filter(user=request.user)
                serializer = CollectionListSerializer(collections, many=True)
                if collections.exists():
                    favourite_genres = self.get_favorite_genres(collections)
                else:
                    favourite_genres = None
                response_data = {
                    "is_success": True,
                    "data": {
                        "collections": serializer.data,
                        "favourite_genres": favourite_genres
                    }
                }
                return Response(response_data)
        except Collection.DoesNotExist:
            return Response("Collection Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = CollectionSerializer(data=request.data)
            if serializer.is_valid():
                if Collection.objects.filter(user=request.user, title=request.data['title']).exists():
                    return Response("A collection with this title already exists for this user.", status=status.HTTP_400_BAD_REQUEST)
                collection = serializer.save(user=request.user)
                return Response({'collection_uuid': str(collection.uuid)}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid):
        try:
            collection = Collection.objects.get(uuid=uuid)
            serializer = CollectionSerializer(collection, data=request.data)
            if serializer.is_valid():
                if Collection.objects.filter(user=request.user, title=request.data['title']).exists():
                    return Response("A collection with this title already exists for this user.", status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response({'collection_uuid': str(collection.uuid)})  # Since no response was given returned uuid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Collection.DoesNotExist:
            return Response("Collection Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        try:
            collection = Collection.objects.get(uuid=uuid)
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response("Collection Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get_favorite_genres(self, collections):
        genres_counter = Counter()
        for collection in collections:
            for movie in collection.movies.all():
                genres = movie.genres.split(',')
                genres_counter.update(genres)
        top_genres = [genre for genre, count in genres_counter.most_common(3)]
        return ','.join(top_genres)

class RequestCountView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            request_count = RequestCounterMiddleware.get_request_count()
            return Response({'requests': request_count})
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class ResetRequestCountView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            RequestCounterMiddleware.reset_request_count()
            return Response({'message': 'request count reset successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)