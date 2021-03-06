# Generated by Django 3.0.5 on 2020-04-17 12:34

from django.db import migrations, models
import video_encoding.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='name',
        ),
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.FloatField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='height',
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='width',
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='db_file',
            field=video_encoding.fields.VideoField(height_field='height', upload_to='', width_field='width'),
        ),
    ]
