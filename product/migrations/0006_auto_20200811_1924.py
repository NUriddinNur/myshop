# Generated by Django 3.0.8 on 2020-08-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('True', 'Mavjud'), ('False', 'Mavjud Emas')], default='True', max_length=15),
        ),
    ]