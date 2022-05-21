# Generated by Django 3.2.7 on 2021-10-27 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_review_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('at', 'Active'), ('cp', 'Completed'), ('dl', 'Delivered'), ('cd', 'Canceled'), ('lt', 'Late')], default='at', max_length=2, verbose_name='Status'),
        ),
    ]