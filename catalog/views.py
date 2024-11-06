from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from catalog.models import Product


def home(request):
    products_list = Product.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products_list, 3)
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "title": "Каталог"
    }
    return render(request, 'home.html', context)


def contacts(request):
    context = {"title": "Контакты"}
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'contacts.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product, "title": f"Товар №{pk}"}
    return render(request, 'product_details.html', context)

