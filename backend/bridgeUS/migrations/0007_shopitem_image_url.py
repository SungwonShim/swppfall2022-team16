# Generated by Django 4.1.2 on 2022-11-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridgeUS', '0006_shopitem_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitem',
            name='image_url',
            field=models.TextField(null=True),
        ),
    ]
