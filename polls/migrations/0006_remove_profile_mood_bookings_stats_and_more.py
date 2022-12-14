# Generated by Django 4.0 on 2022-09-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_profile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mood',
        ),
        migrations.AddField(
            model_name='bookings',
            name='stats',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('Normal', 'Normal'), ('Premium', 'Premium')], default='Normal', max_length=100),
        ),
    ]
