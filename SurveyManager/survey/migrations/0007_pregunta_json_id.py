# Generated by Django 2.1.2 on 2018-11-27 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20181127_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='json_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
