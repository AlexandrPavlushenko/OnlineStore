from catalog.models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .forms import ProductForm, ContactForm

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    paginate_by = 3
    queryset = Product.objects.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.paginate_by:
            paginator = context['paginator']
            context['is_paginated'] = paginator.num_pages > 1
        return context


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'product_details.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('catalog:home')


class ContactsView(FormView):
    template_name = 'contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        return super().form_valid(form)
