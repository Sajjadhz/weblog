# Generated by Django 3.1.5 on 2021-01-25 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210125_1236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['parent__id', 'position'], 'verbose_name': 'دسته بندي', 'verbose_name_plural': 'دسته بندي ها'},
        ),
    ]
