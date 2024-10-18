from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)  # Name of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product
    description = models.TextField()  # Description of the product
    image = models.URLField(max_length=255)  # URL of the product image
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # Link to a category
    created_at = models.DateTimeField(auto_now_add=True)  # Time when the product was added

    def __str__(self):
        return self.name  # Show the product name in the admin panel



class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    




class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

   


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # To link the cart to a session (for non-authenticated users)
    items = models.ManyToManyField(OrderItem)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
   
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    def calculate_total(self):
        """Calculate total price based on items."""
        total = sum([item.product.price * item.quantity for item in self.items.all()])
        self.total_price = total
        self.save()




