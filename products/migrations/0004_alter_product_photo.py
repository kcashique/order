# Generated by Django 4.0.7 on 2022-12-18 21:57

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_updater_alter_product_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='products/', verbose_name='Photo'),
        ),
    ]
