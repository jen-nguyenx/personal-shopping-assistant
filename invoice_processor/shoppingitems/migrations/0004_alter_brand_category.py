# Generated by Django 5.0.4 on 2024-04-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingitems', '0003_alter_brand_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='category',
            field=models.CharField(choices=[('vitamins', 'Vitamins'), ('beauty', 'Beauty'), ('skin-care', 'Skincare'), ('baby-care', 'Babycare'), ('cosmetics', 'Cosmetics'), ('unknown', 'Unknown')], max_length=20),
        ),
    ]
