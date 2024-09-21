from django.core.paginator import Paginator

from django.shortcuts import get_list_or_404, get_object_or_404

from django.shortcuts import render
from django.views.generic import DetailView, ListView

from goods.models import Products, TagPost
from goods.utils import q_search

class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by("-id")
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3
    allow_empty = False
    # чтоб удобно передать в методы
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = get_list_or_404(super().get_queryset().filter(category__slug=category_slug))

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        return context



class ProductView(DetailView):
    # model = Products
    template_name = 'goods/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

# class TagPostListView(ListView):
#     model = Products
#     template_name = "goods/catalog.html"
#     context_object_name = "goods"
#     paginate_by = 3
#     allow_empty = False
#     slug_url_kwarg = "tag_slug"  # Чтобы извлекать slug тега из URL
#
#     def get_queryset(self):
#         # Получаем slug тега из URL
#         tag_slug = self.kwargs.get(self.slug_url_kwarg)
#         # Находим тег, если он существует, или возвращаем 404
#         tag = get_object_or_404(TagPost, slug=tag_slug)
#         # Фильтруем товары по тегу
#         goods = Products.objects.filter(tags__slug=tag_slug)
#         return goods
#
#     def get_context_data(self, **kwargs):
#         # Получаем контекст через базовый класс
#         context = super().get_context_data(**kwargs)
#         # Получаем slug тега и тег для заголовка
#         tag_slug = self.kwargs.get(self.slug_url_kwarg)
#         tag = get_object_or_404(TagPost, slug=tag_slug)
#         # Добавляем дополнительные данные в контекст
#         context['title'] = f'Посты с тегом: {tag.tag}'
#         context['cat_selected'] = None
#         context['category_slug'] = tag_slug
#         return context

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

# def catalog(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
#
#     if category_slug == "all":
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))
#
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#
#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)
#
#     paginator = Paginator(goods, 3)
#
#     current_page = paginator.page(int(page))
#
#
#     context: dict = {
#         'title': "Home - Каталог",
#         "goods": current_page,
#         "category_slug": category_slug
#
#     }
#
#     return render(request, 'goods/catalog.html', context)

# def product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)
#
#     context = {
#         'product': product
#     }
#
#     return render(request, 'goods/product.html', context)


class TagPostListView(ListView):
    model = Products
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'  # Имя переменной в шаблоне
    paginate_by = 3  # Количество постов на одной странице

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        tag = get_object_or_404(TagPost, slug=tag_slug)
        return Products.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['tag_slug']
        tag = get_object_or_404(TagPost, slug=tag_slug)
        context['title'] = f'Посты с тегом: {tag.tag}'
        context['cat_selected'] = None
        context['category_slug'] = tag_slug
        return context