# Generated by Django 3.2.7 on 2021-10-24 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_delete_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellergame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_games', to='games.game'),
        ),
    ]