# Generated by Django 3.1.4 on 2023-07-24 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0004_auto_20230724_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emptybasketrouteschema',
            name='platform_info',
            field=models.OneToOneField(help_text='站台id', on_delete=django.db.models.deletion.CASCADE, related_name='p_route', to='basics.platforminfo', verbose_name='站台id'),
        ),
        migrations.AlterField(
            model_name='emptycacherouteschema',
            name='cache_info',
            field=models.OneToOneField(help_text='堆栈id', on_delete=django.db.models.deletion.CASCADE, related_name='c_route', to='basics.cachedeviceinfo', verbose_name='堆栈id'),
        ),
    ]
