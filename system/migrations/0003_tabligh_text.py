# Generated by Django 2.2.3 on 2019-07-30 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20190730_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabligh',
            name='text',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
