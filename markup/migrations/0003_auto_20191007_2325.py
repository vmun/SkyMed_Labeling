# Generated by Django 2.2.6 on 2019-10-07 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markup', '0002_auto_20191007_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='folder',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='markup.Folder'),
        ),
    ]
