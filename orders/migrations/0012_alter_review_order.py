# Generated by Django 3.2.7 on 2021-10-25 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20211025_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='orders.order'),
        ),
    ]