# Generated by Django 4.1.11 on 2024-02-15 16:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoFileModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.CharField(default='no_name', max_length=50)),
                ('process_status', models.IntegerField(choices=[(1, 'Initial'), (2, 'Processing'), (3, 'End')], default=1)),
                ('processing_success', models.CharField(choices=[('null', 'Null'), ('true', 'True'), ('false', 'False')], default='null', max_length=10)),
                ('file', models.FileField(upload_to='media/')),
            ],
        ),
    ]
