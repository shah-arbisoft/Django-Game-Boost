# Generated by Django 3.2.7 on 2021-09-22 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_first_name_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cnic',
            field=models.CharField(blank=True, default='XXXXX-XXXXXXX-X', max_length=15),
        ),
    ]