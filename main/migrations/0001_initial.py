# Generated by Django 3.2.16 on 2022-11-23 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('public_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
    ]
