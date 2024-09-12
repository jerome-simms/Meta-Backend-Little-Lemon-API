from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, MenuItem, Cart, Order, OrderItem
from .permissions import ManagerPermission
from .serializers import (
    CategorySerializer, 
    MenuItemSerializer,
    CartSerializer, 
    OrderSerializer, 
    OrderItemSerializer,
    UserSerializer
)

##################
# MENU ITEMS VIEWS
##################

class MenuItemsListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [ManagerPermission()]


class MenuItemsModifyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [ManagerPermission()]
        

#################################
# MANAGER AND DELIVERY CREW VIEWS
#################################

class ManagersListCreateDeleteView(views.APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        queryset = User.objects.filter(groups__name__in=['manager'])
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data.get('id')
        user = User.objects.get(id=user_id)
        if user:
            group = Group.objects.get(name='manager')
            user.groups.add(group)
            data = {'message': f'User with id {user_id} upgraded to manager'}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.data.get('id')
        user = User.objects.get(id=user_id)
        if user:
            group = Group.objects.get(name='manager')
            user.groups.remove(group)
            data = {'message': f'User with id {user_id} removed from manager group'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name__in=['delivery_crew'])
    serializer_class = UserSerializer
    permission_classes = [ManagerPermission]

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        user = User.objects.get(id=user_id)
        if user:
            group = Group.objects.get(name='delivery_crew')
            user.groups.add(group)
            data = {'message': f'User with id {user_id} added to delivery_crew group'}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class DeliveryCrewDeleteView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name__in=['delivery_crew'])
    serializer_class = UserSerializer
    permission_classes = [ManagerPermission]

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        if user:
            group = Group.objects.get(name='delivery_crew')
            user.groups.remove(group)
            data = {'message': f'User with id {user_id} removed from delivery_crew group'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


######################
# CART AND ORDER VIEWS
######################

class CartAPIView(views.APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated()]

    def get(self, request):
        if request.user:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart_items = Cart.objects.all()
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
        item_id = request.data.get('item_id')
        menu_item = MenuItem.objects.get(id=item_id)
        quantity = int(request.data.get('quantity', 1))
        if menu_item:
            Cart.objects.create(
                user=request.user,
                menuitem=menu_item,
                quantity=quantity, 
                unit_price=menu_item.price,
                price=quantity*menu_item.price
            )
            serializer = CartSerializer(Cart.objects.filter(user=request.user), many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        # Deletes all menu items created by the current user token
        queryset = Cart.objects.filter(user=request.user)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrdersAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # check if the request is from a manager, then delivery crew and then customer respectively
        current_user = request.user
        if current_user.groups.filter(name__in=['manager']).exists():
            queryset = Order.objects.all()
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif current_user.groups.filter(name__in=['delivery_crew']).exists():
            # gets all the items assigned to the current user who is a member of the delivery crew
            queryset = Order.objects.filter(delivery_crew=current_user)
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # this must be a customer
            queryset = OrderItem.objects.filter(order__user=request.user)
            if not queryset:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = OrderItemSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        new_order = Order.objects.create(
            user=request.user,
            total=0
        )
        
        user_cart_items = Cart.objects.filter(user=request.user)
        running_total = 0
        # create an orderItem for each item in cart
        for item in user_cart_items:
            OrderItem.objects.create(
                order=new_order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
            running_total += item.price
        
        new_order.total = running_total
        new_order.save()
        user_cart_items.delete()

        data = {'message': 'Successfully added cart items to order'}
        return Response(data, status=status.HTTP_201_CREATED)
    
  
class OrderView(views.APIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_permissions(self):
        if self.request.method == 'delete':
            return [ManagerPermission()]
        return []
    
    def get(self, request, *args, **kwargs):
        # handling an order for a customer
        order_id = self.kwargs['pk']
        
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            data = {'message': 'Order with provided Order ID not found'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
        if order.user.id != request.user.id:
            data = {'message': 'You do not have permission to view this order'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
        items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # TODO: this method needs to be refactored for better readability and simplicity
    def patch(self, request, *args, **kwargs):
        # Only allow for the delivery_crew and status to be changed
        order_id = self.kwargs['pk']
        order = None
        if request.user.groups.filter(name__in=['manager']).exists():
            delivery_crew_id = request.data.get('delivery_crew_id', None)
            if delivery_crew_id:
                try:
                    order = Order.objects.get(id=order_id)
                    delivery_crew = User.objects.get(id=delivery_crew_id)
                except (Order.DoesNotExist, User.DoesNotExist):
                    return Response(status=status.HTTP_404_NOT_FOUND)

                order.delivery_crew = delivery_crew
                order.save()

            order_status = request.data.get('status', None)
            if order_status:
                if not order:
                    try:
                        order = Order.objects.get(id=order_id)
                    except Order.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                
                order.status = order_status
                order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        elif request.user.groups.filter(name__in=['delivery_crew']).exists():
            # Only allow the delivery crew to update the status
            order_status = request.data.get('status', None)
            try:
                order_status = int(order_status) # order status should be a 1 or 0
                if order_status > 1 or order_status < 0:
                    raise ValueError
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if order_status:
                if not order:
                    try:
                        order = Order.objects.get(id=order_id)
                    except Order.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                
                order.status = order_status
                order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['manager']).exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        data = {'message': f'Order with id {order_id} successfully deleted'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    