# Generated by Django 3.1.2 on 2021-09-20 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date and time this object was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date and time this object was last modified.')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date and time this object was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date and time this object was last modified.')),
                ('name', models.CharField(max_length=256)),
                ('org_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisation.group')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisation.organisation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
