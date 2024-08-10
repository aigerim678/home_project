
from django.http import HttpResponse
from django.shortcuts import render

def catalog(request):
    context: dict = {
        'title': "Home - Главная",
        "content": "Магазин мебели HOME"

    }

    return render(request, 'goods/catalog.html', context)


def product(request):
    context: dict = {
        'title': "Home - О нас",
        "content": "О нас",
        "text_on_page": "Текст о магазине"

    }

    return render(request, 'goods/product.html', context)