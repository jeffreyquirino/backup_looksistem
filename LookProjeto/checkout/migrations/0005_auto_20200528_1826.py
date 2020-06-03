# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-05-28 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20200527_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('deposit', 'Depósito'), ('pagseguro', 'PagSeguro'), ('paypal', 'Paypal')], default='deposit', max_length=20, verbose_name='Opção de Pagamento'),
        ),
    ]
