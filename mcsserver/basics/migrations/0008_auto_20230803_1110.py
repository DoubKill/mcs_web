# Generated by Django 3.1.4 on 2023-08-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0007_platforminfo_wet_group_threshold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='value',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]