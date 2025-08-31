from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^(\+\d{1,15}|\d{3}-\d{3}-\d{4})$',
                message="Phone must be in format +1234567890 or 123-456-7890"
            )
        ]
    )

    def __str__(self):
        return f"{self.name} ({self.email})"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def calculate_total(self):
        return sum(p.price for p in self.products.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_amount = self.calculate_total()
        super().save(update_fields=["total_amount"])
