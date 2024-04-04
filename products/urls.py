from django.urls import path
from . import views


urlpatterns = [
 path('product/<int:pk>/<slug:slug>/', views.Product_Page, name='product'),
]