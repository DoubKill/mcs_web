# Generated by Django 3.1.4 on 2023-10-13 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0014_cachedeviceinfo_is_connected'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgvType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_ID', models.CharField(max_length=256)),
                ('type_name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'AGV类型',
                'verbose_name_plural': 'AGV类型',
                'db_table': 'bdm_agv_type',
            },
        ),
        migrations.AddField(
            model_name='workarea',
            name='agv_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basics.agvtype'),
        ),
    ]
