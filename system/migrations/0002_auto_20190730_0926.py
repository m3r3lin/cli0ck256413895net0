# Generated by Django 2.2.3 on 2019-07-30 04:56

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_ferestande', models.CharField(max_length=30, unique=True)),
                ('code_girande', models.CharField(max_length=30, unique=True)),
                ('onvan', models.CharField(max_length=30, unique=True)),
                ('text', models.TextField(blank=True, max_length=255, null=True)),
                ('tarikh', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='kife_daramad',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999999999, message='کیف درآمد نمیتواند بیشتر از 9999999999 باشد. ')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='kife_pool',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999999999, message='کیف پول نمیتواند بیشتر از 9999999999 باشد. ')]),
        ),
    ]
