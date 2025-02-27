# Generated by Django 5.1.6 on 2025-02-24 22:56

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=20, null=True, unique=True)),
                ('course_name', models.CharField(max_length=200, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('id_number', models.CharField(max_length=50, null=True, unique=True)),
                ('phone', models.CharField(max_length=50, null=True, unique=True)),
                ('email', models.EmailField(max_length=50, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('face_encoding', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_code', models.CharField(max_length=20, null=True, unique=True)),
                ('unit_name', models.CharField(max_length=200, null=True)),
                ('teaching_hrs_per_class', models.PositiveIntegerField(null=True)),
                ('teaching_hrs_week', models.PositiveIntegerField(null=True)),
                ('teaching_hrs_term', models.PositiveIntegerField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['unit_name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_examination_officer', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='StudentExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.series')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.studentexam')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.trainer')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.unit')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in', models.DateTimeField(blank=True, null=True)),
                ('clock_out', models.DateTimeField(blank=True, null=True)),
                ('roll', models.CharField(max_length=20, null=True)),
                ('clock_in_status', models.BooleanField(default=False)),
                ('clock_out_status', models.BooleanField(default=False)),
                ('time_taken', models.PositiveIntegerField(blank=True, null=True)),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.unit')),
            ],
            options={
                'ordering': ['-clock_in', '-clock_out'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_mark', models.PositiveIntegerField(null=True)),
                ('exam_mark', models.PositiveIntegerField(null=True)),
                ('project_mark', models.PositiveIntegerField(null=True)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.series')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.studentexam')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.unit')),
            ],
        ),
        migrations.CreateModel(
            name='CourseUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.course')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.unit')),
            ],
        ),
    ]
