from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User
from django.shortcuts import reverse



# Create your models here.
class Product(models.Model):
    productname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    photo = VersatileImageField('Photo',blank=True,null=True,upload_to="products/")
    creator = models.ForeignKey(
        User,
        related_name="creator_%(class)s_objects",
        blank=True,
        on_delete=models.CASCADE,
    )
    updater = models.ForeignKey(
        User,
        related_name="updater_%(class)s_objects",
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.productname)

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={
            'id': self.id
        })
    
    def edit_product_url(self):
        return reverse("products:edit", kwargs={
            'id': self.id
        })
    
    def delete_product_url(self):
        return reverse("products:product_delete", kwargs={
            'id': self.id
        })

    def get_add_to_cart_url(self):
        return reverse("products:add-to-cart", kwargs={
            'id': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("products:remove-from-cart", kwargs={
            'id': self.id
        })


class OrderItem(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE,
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.productname}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
