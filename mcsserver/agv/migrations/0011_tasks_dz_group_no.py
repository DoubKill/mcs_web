# Generated by Django 3.1.4 on 2023-09-26 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agv', '0010_cachedevicestock_storge_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='dz_group_no',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
