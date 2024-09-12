from django.urls import path

from . import views


urlpatterns = [
    # menu items
    path('menu-items', views.MenuItemsListCreateView.as_view()), 
    path('menu-items/<int:pk>', views.MenuItemsModifyView.as_view()), 

    # manager views
    # path('groups/manager/users', views.ManagerDeleteView.as_view()), 
    path('groups/manager/users', views.ManagersListCreateDeleteView.as_view()), 
    # path('groups/manager/users/<int:pk>', views.ManagerDeleteView.as_view()), 
    
    path('groups/delivery-crew/users', views.DeliveryCrewListCreateView.as_view()), 
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewDeleteView.as_view()), 

    # customer cart views
    path('cart/menu-items', views.CartAPIView.as_view()), 

    # order views
    path('orders', views.OrdersAPIView.as_view()), 
    path('orders/<int:pk>', views.OrderView.as_view()), 
]