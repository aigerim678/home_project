from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Products


def catalog(request):
    goods = Products.objects.all()
    context: dict = {
        'title': "Home - Каталог",
        "goods": goods,

    }

    return render(request, 'goods/catalog.html', context)


def product(request):
    context: dict = {
        'title': "Home - О нас",
        "content": "О нас",
        "text_on_page": "Текст о магазине"

    }

    return render(request, 'goods/product.html', context)
