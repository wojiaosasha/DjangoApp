# Generated by Django 3.2.16 on 2022-11-23 10:25

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_parent_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='public_name',
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=20)),
                ('sizes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=20)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='images'), size=7)),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('discount_price', models.IntegerField(null=True)),
                ('is_new', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.category')),
            ],
        ),
    ]
