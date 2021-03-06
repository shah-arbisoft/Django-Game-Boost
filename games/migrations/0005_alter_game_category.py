# Generated by Django 3.2.7 on 2021-10-01 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_game_dummy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.ManyToManyField(related_name='categories', related_query_name='games', to='games.Category'),
        ),
    ]
