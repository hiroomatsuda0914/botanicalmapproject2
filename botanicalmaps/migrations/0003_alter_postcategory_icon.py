# Generated by Django 4.0.2 on 2023-05-17 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botanicalmaps', '0002_alter_mountainarea_mountain_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategory',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', verbose_name='アイコン'),
        ),
    ]
