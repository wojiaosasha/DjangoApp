# Generated by Django 3.2.16 on 2022-12-19 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_is_leaf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='cart',
            new_name='old_cart',
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.amount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser')),
            ],
        ),
    ]
