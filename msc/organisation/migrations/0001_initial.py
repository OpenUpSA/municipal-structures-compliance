# Generated by Django 3.1.2 on 2021-09-08 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date and time this object was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date and time this object was last modified.')),
                ('name', models.CharField(max_length=256)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisation.organisation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]