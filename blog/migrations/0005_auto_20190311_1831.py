# Generated by Django 2.0 on 2019-03-11 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190311_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readed_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='readed_num',
        ),
        migrations.AddField(
            model_name='readnum',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog'),
        ),
    ]
