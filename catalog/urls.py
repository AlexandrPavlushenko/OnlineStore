from django.urls import path
from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts', views.contacts, name='contacts'),
    path('catalog/<int:pk>', views.product_details, name='product_details'),
    path('add_product', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category')
]