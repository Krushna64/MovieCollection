from django.urls import path
from .views import RegisterView, MovieView, CollectionView, RequestCountView, ResetRequestCountView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('movies/', MovieView.as_view(), name='movies'),
    path('collection/', CollectionView.as_view(), name='collection_list'),
    path('collection/<uuid:uuid>/', CollectionView.as_view(), name='collection_detail'),
    path('request-count/', RequestCountView.as_view(), name='request_count'),
    path('request-count/reset/', ResetRequestCountView.as_view(), name='reset_request_count'),
]
