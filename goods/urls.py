from django.urls import path
from goods import views

app_name = "goods"
urlpatterns = [
    path("search/", views.catalog, name='search'),
    path("<slug:category_slug>/", views.catalog, name='index'),
    path("", views.catalog, name='index'),  # Handle no category_slug case
    path("product/<slug:product_slug>/", views.product, name='product'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag')
]

