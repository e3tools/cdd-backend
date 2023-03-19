# Generated by Django 4.0.4 on 2022-10-13 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process_manager', '0003_activity_description_activity_order_activity_phase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='activity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='process_manager.activity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='phase',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='process_manager.phase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='process_manager.project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='total_tasks',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
