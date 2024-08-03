from django.urls import path

from users.views import UserRegisterView, UserDetailView, CustomLoginView, CustomLogoutView

urlpatterns = [
    # Authentication
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # User management
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
