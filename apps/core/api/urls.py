from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.users.api.urls')),
    path('company/', include('apps.company.api.urls')),
]
