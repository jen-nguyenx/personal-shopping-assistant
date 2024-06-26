from django.db import models

class Brand(models.Model):
        BRAND_CATEGORIES = [
             ('vitamins', 'Vitamins'),
             ('beauty', 'Beauty'),
             ('skin-care', 'Skincare'),
             ('baby-care', 'Babycare'),
             ('cosmetics', 'Cosmetics'),
             ('unknown', 'Unknown')
        ]

        name = models.CharField(max_length=50)
        category = models.CharField(max_length=20, choices=BRAND_CATEGORIES)

        def __str__(self):
             return f'{self.name} ({self.get_category_display()})'


class Product(models.Model):
     name = models.CharField(max_length=255, unique=True)
     weight = models.DecimalField(max_digits=5, decimal_places=2)

     def __str__(self):
          return f'{self.name} {self.weight}'


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price_aud = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product
