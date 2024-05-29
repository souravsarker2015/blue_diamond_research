from django.urls import path

from apps.company.api import views

urlpatterns = [
    path('create/', views.CompanyCreate.as_view(), name='company_create'),
    path('list/', views.CompanyListApiView.as_view(), name='company_list'),
    path('details/<uuid:pk>/', views.CompanyRetrieveAPIView.as_view(), name='company_details'),
    path('update/<uuid:pk>/', views.CompanyUpdateApiView.as_view(), name='company_update'),
    path('delete/<uuid:pk>/', views.CompanyDestroyAPIView.as_view(), name='company_delete'),

]
