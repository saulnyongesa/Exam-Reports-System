# Generated by Django 5.1.6 on 2025-02-07 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_mark_cat_mark_alter_mark_exam_mark_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentexam',
            name='series',
        ),
    ]
