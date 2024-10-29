from django.urls import path
from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/home/', views.home, name='home'),
    path('catalog/contacts/', views.contacts, name='contacts'),
]