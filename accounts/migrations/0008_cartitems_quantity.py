# Generated by Django 4.1.7 on 2023-05-02 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_cart_razor_pay_order_id_cart_razor_pay_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
