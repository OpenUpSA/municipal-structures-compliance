# Generated by Django 3.1.2 on 2021-09-03 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='input_type',
            field=models.CharField(choices=[('dropdown', 'Dropdown'), ('shorttext', 'Shorttext'), ('longtext', 'Longtext'), ('checkbox', 'Checkbox'), ('radio', 'Radio'), ('number', 'Number')], db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='question',
            name='instruction',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
    ]
