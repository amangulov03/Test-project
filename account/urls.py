from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView, ActivateView, CustomTokenObtainPairView, ProfileView, LoginLogListView

urlpatterns = [ 
    path('api/v1/users/register/', RegisterUserView.as_view()),
    path('api/v1/account/activate/', ActivateView.as_view()),

    path('api/v1/auth/token/', CustomTokenObtainPairView.as_view()),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/users/me/', ProfileView.as_view()),
    path('api/v1/logs/login/', LoginLogListView.as_view())
]