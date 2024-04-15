from django.db import models

class ShoppingItems(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    price_aud = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Brands(models.Model):
        BRAND_CATEGORIES = [
             ('Vitamins', 'Vitamins'),
             ('Beauty', 'Beauty'),
             ('Skincare', 'Skincare'),
             ('Babycare', 'Babycare'),
             ('Cosmetics', 'Cosmetics')
        ]

        name = models.CharField(max_length=50)
        category = models.CharField(max_length=20, choices=BRAND_CATEGORIES)

        def __str__(self):
             return f'{self.name} ({self.get_category_display()})'