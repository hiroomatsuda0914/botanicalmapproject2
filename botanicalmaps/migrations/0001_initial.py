# Generated by Django 4.0.2 on 2023-05-08 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(max_length=20, verbose_name='エリア')),
            ],
        ),
        migrations.CreateModel(
            name='MountainArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mountain_name', models.CharField(max_length=20, verbose_name='山域')),
                ('mountain_latitude', models.FloatField(verbose_name='山の緯度')),
                ('mountain_longitude', models.FloatField(verbose_name='山の経度')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='botanicalmaps.area', verbose_name='エリア')),
            ],
        ),
        migrations.CreateModel(
            name='PlantName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plantname', models.CharField(max_length=30, verbose_name='植物名')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30, verbose_name='カテゴリ')),
                ('icon', models.ImageField(upload_to='icons', verbose_name='アイコン')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
                ('shooting_date', models.DateTimeField(verbose_name='撮影日')),
                ('photo_latitude', models.FloatField(verbose_name='写真の緯度')),
                ('photo_longitude', models.FloatField(verbose_name='写真の経度')),
                ('photo', models.ImageField(upload_to='photos', verbose_name='写真')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='コメント')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='botanicalmaps.area', verbose_name='エリア')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='botanicalmaps.postcategory', verbose_name='カテゴリ')),
                ('mountain_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='botanicalmaps.mountainarea', verbose_name='山域')),
                ('plantname', models.ManyToManyField(blank=True, to='botanicalmaps.PlantName', verbose_name='植物名')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー名')),
            ],
        ),
    ]
