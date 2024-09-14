from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404

from goods.models import Products, TagPost
from goods.utils import q_search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)

    current_page = paginator.page(page)


    context: dict = {
        'title': "Home - Каталог",
        "goods": current_page,
        "category_slug": category_slug

    }

    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }

    return render(request, 'goods/product.html', context)


def show_tag_postlist(request, tag_slug):
    page = request.GET.get('page', 1)
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = get_list_or_404(Products.objects.filter(tags__slug=tag_slug))

    paginator = Paginator(posts, 3)

    current_page = paginator.page(page)
    context = {
        'title': f'Посты с тегом: {tag.tag}',
        'goods': current_page,  # Передаем все посты без пагинации
        'cat_selected': None,
        'category_slug': tag_slug
    }

    return render(request, 'goods/catalog.html', context)