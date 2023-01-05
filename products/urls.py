from django.urls import path

from . import views
# from .views import OrderSummaryView


app_name = "products"

urlpatterns = [
    path("home", views.homepage, name="homepage"),

    path("create/", views.create_view, name="create"),
    path("products/", views.list_view, name="product_list"),
    path("edit/<str:id>/", views.update_view, name="edit"),
    path("view/<str:id>/", views.detail_view, name="product_detail"),
    path("delete/<str:id>/", views.delete_view, name="product_delete"),

    path('order-summary/', views.order_summary, name='order-summary'),
    path('add-to-cart/<id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<id>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<id>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]
