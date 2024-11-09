from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from catalog.models import Product, Category
from django.contrib import messages


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


def add_product(request):
    category_list = Category.objects.all()
    context = {"title": "Добавление товара", "category_list": category_list}

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')
        price = request.POST.get('price')

        if Product.objects.filter(name=name).exists():
            messages.error(request, " Товар с таким именем уже существует.")

        else:
            category = Category.objects.get(id=category_id)
            product = Product(
                name=name,
                description=description,
                image=image,
                category=category,
                price=price
            )
            product.save()

            messages.success(request, " Товар успешно добавлен!")

    return render(request, 'add_product.html', context)


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('new_category_name')
        description = request.POST.get('description_category')

        if category_name:
            category, created = Category.objects.update_or_create(
                name=category_name,
                defaults={'description': description}
            )
            return JsonResponse({'id': category.id, 'name': category.name, 'created': created})

    return JsonResponse({'error': 'Invalid data'}, status=400)
