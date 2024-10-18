from django.shortcuts import render
from django.contrib.sessions.models import Session
from .models import Product, Category
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Order, OrderItem
from rest_framework.exceptions import NotFound
from django.db import models
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from django.http import JsonResponse






# View for the homepage that lists all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

# View for displaying all products in a category
def product_list(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})

# API View to get the list of categories (to be consumed by frontend)
class CategoryListView(APIView):
    permission_classes = [AllowAny]  # No authentication required
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET'])  # Ensure this decorator is applied for API views
@permission_classes([AllowAny])
def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    
    # Log the serialized data to verify
    print(f"Serialized products: {serializer.data}")
    
    return Response(serializer.data) # Ensure you're returning a DRF Response object



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_data = {
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'image': product.image,
        'category': product.category.name,
        'created_at': product.created_at
    }
    return JsonResponse(product_data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_order(request):
    data = request.data
    id = data.get('id')
    quantity = data.get('quantity', 1)
    user = request.user
   
    
    products = data.get('products', [])

    if not products:
        return Response({'error': 'No products provided'}, status=status.HTTP_400_BAD_REQUEST)

    order, created = Order.objects.get_or_create(user=user)

    total_price = 0

    for product_data in products:
        product_id = product_data.get('id')
        quantity = product_data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)

        # Create a new OrderItem for each product
        order_item, created = OrderItem.objects.get_or_create(
            product=product,
            quantity=quantity
        )

        # Add the OrderItem to the order
        order.items.add(order_item)

        # Update the total price
        total_price += product.price * quantity

    # Save the total price in the order
    order.total_price = total_price
    order.save()

    return Response({'message': 'Products added to order for user', 'total_price': total_price}, status=status.HTTP_201_CREATED)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order(request):
    user = request.user
    


    order_items = Order.objects.filter(user=user)
    items = []
    total_price = 0
    
    for order_item in order_items:

        product = order_item.product
        item_price = order_item.quantity * product.price
        total_price += item_price
        

        items.append({
            'id': product.id,
            'name': product.name,
            'quantity': order_item.quantity,
            'price': product.price,
            'item_price': item_price,
        })

        print(f"Total price before saving: {total_price}")
        

    return Response({'items': items, 'total_price': total_price}, status=status.HTTP_200_OK)


