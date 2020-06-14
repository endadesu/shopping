# Generated by Django 3.0.5 on 2020-05-09 01:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmodel',
            name='customerId',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='itemId',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='numberOfItem',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='images',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='value',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
