from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from catalog.models import Product
from django.views.generic import ListView, View


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'page_obj'
    paginate_by = 3
    title = "Каталог"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.paginate_by:
            paginator = context['paginator']
            context['is_paginated'] = paginator.num_pages > 1
        context['title'] = self.title
        return context


class ContactsView(View):
    template_name = 'contacts.html'
    title = "Контакты"

    def get(self, request):
        context = {"title": self.title}
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class ProductDetailsView(View):
    template_name = 'product_details.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {"product": product, "title": f"Товар №{pk}"}
        return render(request, self.template_name, context)
