from re import template
from django.urls import path
from django.views.generic import TemplateView

from .views import Like, ProductDescription, Ping, ProductName, Product, ProductTrigram

urlpatterns = [
    path("ping", Ping.as_view(), name="ping"),
    path("api/like", Like.as_view(), name="like_search"),
    path("api/product-description", ProductDescription.as_view(), name="fts_product_description"),
    path("api/product-name", ProductName.as_view(), name="fts_product_name"),
    path("api/product", Product.as_view(), name="fts_product_all"),
    path("api/product-trgm", ProductTrigram.as_view(), name="fts_product_all_trigram")
]