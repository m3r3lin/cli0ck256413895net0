# Generated by Django 2.2.3 on 2019-08-02 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20190802_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code_moaref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
