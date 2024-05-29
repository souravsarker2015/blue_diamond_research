from django.urls import path

from apps.users.api import views

urlpatterns = [
    path('token2/', views.CustomTokenView.as_view(), name='token2'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
]
