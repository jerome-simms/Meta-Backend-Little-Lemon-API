from django.urls import path

from .views import MenuItemsView, MenuItemView

urlpatterns = [
    path('menu-items', MenuItemsView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', MenuItemView.as_view(), name='menu-item'),
]