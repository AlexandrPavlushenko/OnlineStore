from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    HomeView,
    ContactsView,
    ProductDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView, CategoryProductsView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("catalog/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("catalog/create/", ProductCreateView.as_view(), name="product_create"),
    path("catalog/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path(
        "catalog/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]
