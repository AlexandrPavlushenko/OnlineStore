from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.paginate_by:
            paginator = context['paginator']
            context['is_paginated'] = paginator.num_pages > 1
        return context


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'category', 'image']
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = None  # Не существует объекта продукта при создании
        return context

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'description', 'category', 'image']
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object  # Передаём объект продукта в контекст
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('catalog:home')  # Куда перенаправить после успешного удаления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object  # Передаём объект продукта в контекст
        return context

class ContactsView(View):
    template_name = 'contacts.html'

    def get(self, request):
        context = {"title": 'Контакты'}
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class ProductDetailsView(View):
    template_name = 'product_details.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {'product': product})

