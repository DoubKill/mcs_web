# Generated by Django 3.1.4 on 2023-07-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0006_auto_20230726_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='platforminfo',
            name='wet_group_threshold',
            field=models.IntegerField(blank=True, help_text='湿式设备组阈值', null=True, verbose_name='湿式设备组阈值'),
        ),
    ]