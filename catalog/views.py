from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from catalog.models import Product, Category
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.urls import reverse_lazy
from .forms import ProductForm, ContactForm, ProductModeratorForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    paginate_by = 3

    def get_queryset(self):
        cache_key = 'all_available_products'
        products = cache.get(cache_key)
        if products is None:
            products = Product.objects.filter(is_available=True)
            cache.set(cache_key, products, 60 * 15)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.paginate_by:
            paginator = context["paginator"]
            context["is_paginated"] = paginator.num_pages > 1
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailsView(DetailView):
    model = Product
    template_name = "product_details.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_class(self):
        if self.request.user.is_superuser:
            return ProductForm
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        return ProductForm

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.can_unpublish_product"
        )

    def handle_no_permission(self):
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.delete_product"
        )

    def handle_no_permission(self):
        raise PermissionDenied


class ContactsView(FormView):
    template_name = "contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        return super().form_valid(form)


class CategoryProductsView(ListView):
    model = Product
    template_name = 'category_products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = Category.objects.get(id=category_id)
        if self.paginate_by:
            paginator = context["paginator"]
            context["is_paginated"] = paginator.num_pages > 1
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id, is_available=True)


