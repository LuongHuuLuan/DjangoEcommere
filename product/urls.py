from django.urls import path
from . import views

urlpatterns = [
    path('api/products', views.ProductListView.as_view()),
    path('api/private/products', views.ProductCRUD.as_view()),
    path('api/private/products/<int:pk>', views.ProductCRUD.as_view()),
]