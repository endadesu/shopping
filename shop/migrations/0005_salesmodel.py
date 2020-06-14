# Generated by Django 3.0.5 on 2020-06-14 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cartmodel_itemvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemId', models.IntegerField(blank=True, default=0, null=True)),
                ('numberOfItem', models.IntegerField(blank=True, default=0, null=True)),
                ('sales', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]