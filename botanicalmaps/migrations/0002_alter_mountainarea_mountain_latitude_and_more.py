# Generated by Django 4.0.2 on 2023-05-17 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botanicalmaps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mountainarea',
            name='mountain_latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='山の緯度'),
        ),
        migrations.AlterField(
            model_name='mountainarea',
            name='mountain_longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='山の経度'),
        ),
    ]
