from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from movies.models import User
from .models import Collection, Movie
from django.test import TestCase


# Create your tests here.
class MovieAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.movie_data = {
            'title': 'Test Movie',
            'description': 'Testing movie creation',
            'genres': 'Action, Adventure'
        }
        self.movie = Movie.objects.create(
            title='Sample Movie',
            description='Sample movie description',
            genres='Drama'
        )

    def test_get_movie_list(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CollectionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.collection_data = {
            'title': 'Test Collection',
            'description': 'Testing collection creation',
            'movies': [
                {
                    "uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d",
                    "title": "Queerama",
                    "description": "50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.",
                    "genres": ""
                },
                {
                    "uuid": "163ce013-03e2-47e9-8afd-e7de7688c151",
                    "title": "Satana likuyushchiy",
                    "description": "In a small town live two brothers, one a minister and the other one a hunchback painter of the chapel who lives with his wife. One dreadful and stormy night, a stranger knocks at the door asking for shelter. The stranger talks about all the good things of the earthly life the minister is missing because of his puritanical faith. The minister comes to accept the stranger's viewpoint but it is others who will pay the consequences because the minister will discover the human pleasures thanks to, ehem, his sister- in -law… The tormented minister and his cuckolded brother will die in a strange accident in the chapel and later an infant will be born from the minister's adulterous relationship.",
                    "genres": ""
                }
            ]  # Replace with actual movie data if needed
        }
        self.collection = Collection.objects.create(
            user=self.user,
            title='Sample Collection',
            description='Sample description'
        )

    def test_create_collection(self):
        response = self.client.post('/collection/', self.collection_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)

    def test_get_collection_list(self):
        response = self.client.get('/collection/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['data']['collections']) > 0)

    def test_get_collection_detail(self):
        response = self.client.get(f'/collection/{self.collection.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_collection(self):
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'movies': [
                {
                    "uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d",
                    "title": "Queerama",
                    "description": "50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.",
                    "genres": ""
                }
            ]  # Replace with updated movie data if needed
        }
        response = self.client.put(f'/collection/{self.collection.uuid}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_collection(self):
        response = self.client.delete(f'/collection/{self.collection.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_favorite_genres(self):
        # Assuming you have movies and collections set up appropriately
        response = self.client.get('/collection/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('favourite_genres', response.data['data'])

class RequestCountAPITest(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_request_count(self):
        # Initial request count should be zero
        response = self.client.get('/request-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requests'], 8)  # API called 8 times hence 8
        # Make another request and check count
        response = self.client.get('/request-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requests'], 9)  # API called 8 times hence 8

    def test_reset_request_count(self):
        # Make a request to increment count
        self.client.get('/request-count/')
        # Reset the request count
        response = self.client.post('/request-count/reset/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'request count reset successfully')
        # Verify count is reset
        response = self.client.get('/request-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requests'], 1)
