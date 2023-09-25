from django.urls import path
from . import views

urlpatterns = [
    path('api/products', views.ProductListView.as_view()),
    path('api/products', views.CreateProductView.as_view()),
    path('api/products/<int:pk>', views.UpdateProductView.as_view()),
]