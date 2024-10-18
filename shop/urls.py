from django.urls import path
from .views import category_list, product_list, CategoryListView 
from .views import products_by_category
from .views import product_detail, add_to_order, view_order
from . import views


urlpatterns = [
    path('categories/', category_list, name='category-list'),  # Existing category list page
    path('products/<int:category_id>/', product_list, name='product-list'),  # Products list for a category
    path('api/categories/', CategoryListView.as_view(), name='api-category-list'),
    path('api/products/<int:category_id>/', products_by_category, name='products-by-category'),
    path('api/product/<int:product_id>/', product_detail, name='product-detail'),
    path('api/order/add/', add_to_order, name='add-to-order'),
    path('api/order/', view_order, name='view-order'),
]
