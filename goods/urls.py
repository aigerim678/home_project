from django.urls import path
from goods import views

app_name = "goods"
urlpatterns = [
    path("search/", views.CatalogView.as_view(), name='search'),
    path("<slug:category_slug>/", views.CatalogView.as_view(), name='index'),
    path("", views.CatalogView.as_view(), name='index'),  # Handle no category_slug case
    path("product/<slug:product_slug>/", views.ProductView.as_view(), name='product'),
    path('tag/<slug:tag_slug>/', views.TagPostListView.as_view(), name='tag')
]

