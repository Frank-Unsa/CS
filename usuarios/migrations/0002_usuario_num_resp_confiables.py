# Generated by Django 3.2.9 on 2021-12-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='num_resp_confiables',
            field=models.IntegerField(null=True),
        ),
    ]
