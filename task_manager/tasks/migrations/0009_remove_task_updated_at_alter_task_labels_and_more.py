# Generated by Django 5.1 on 2024-08-28 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('statuses', '0001_initial'),
        ('tasks', '0008_alter_task_author_alter_task_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='tasks', through='tasks.TaskLabel', to='labels.label', verbose_name='Метки'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='statuses.status', verbose_name='Статус'),
        ),
    ]
