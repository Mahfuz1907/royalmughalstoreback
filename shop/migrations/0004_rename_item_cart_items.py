# Generated by Django 5.1.1 on 2024-10-16 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_cart_user_cart_session_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='item',
            new_name='items',
        ),
    ]
