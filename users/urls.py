from django.urls import path

from users.views import RegisterUserView, UserProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
