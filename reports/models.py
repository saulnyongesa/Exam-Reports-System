from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.utils.timezone import make_aware, is_naive


# USERS=================================================
class User(AbstractUser):
    ADMIN = (
        ("ADMIN", "ADMIN"),
        ("STUDENT", "STUDENT"),
        ("TRAINER", "TRAINER"),
        ("EXAMINATION_OFFICER", "EXAMINATION_OFFICER"),
    )
    id_number = models.CharField(max_length=50, unique=True, null=True)
    role = models.CharField(max_length=50, choices=ADMIN, default="STUDENT")
    profile_photo = models.ImageField(upload_to="photos/", blank=True, null=True)

class OTP(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    otp = models.PositiveIntegerField(null=True, unique=True)
    is_used = models.BooleanField(default=False)
    created_time = models.DateTimeField(null=True)
    expire_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.otp}"

    def save(self, *args, **kwargs):
        self.created_time = datetime.now()
        if not self.created_time:
            self.created_time = datetime.now()
        if not self.expire_time:
            self.expire_time = self.created_time + timedelta(minutes=5)
        super().save(*args, **kwargs)


# EXAM REPORT MODELS===============================================
class Series(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            Series.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_code = models.CharField(max_length=20, null=True, unique=True)
    course_name = models.CharField(max_length=200, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.course_name


class Unit(models.Model):
    unit_code = models.CharField(max_length=20, null=True, unique=True)
    unit_name = models.CharField(max_length=200, null=True)
    teaching_hrs_per_class = models.PositiveIntegerField(null=True)
    teaching_hrs_week = models.PositiveIntegerField(null=True)
    teaching_hrs_term = models.PositiveIntegerField(null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["unit_name"]

    def __str__(self):
        return f"{self.unit_name} --- {self.unit_code}"

    def save(self, *args, **kwargs):
        self.name = self.unit_name.upper()
        super().save(*args, **kwargs)


class CourseUnit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not CourseUnit.objects.filter(course=self.course, unit=self.unit).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.course_name}: UNIT: {self.unit.unit_name}"


class StudentExam(models.Model):
    registration_number = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class StudentSeries(models.Model):
    student = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.registration_number} registered: {self.series}"


class Mark(models.Model):
    student = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    cat_mark = models.PositiveIntegerField(null=True)
    exam_mark = models.PositiveIntegerField(null=True)
    project_mark = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.student} {self.series} {self.cat_mark} {self.exam_mark} {self.project_mark}"

class StudentExamStatus(models.Model):
    student = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    summative_theory = models.CharField(max_length=20, null=True)
    summative_practical = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return f"{self.student.registration_number}  {self.unit} {self.summative_practical} {self.summative_practical}"


# TRAINER MODELS=========================================================


class Trainer(models.Model):
    name = models.CharField(max_length=50, null=True)
    id_number = models.CharField(max_length=50, unique=True, null=True)
    email = models.EmailField(max_length=50, null=True, unique=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    face_encoding = models.TextField(null=True)
    is_active = models.BooleanField(default=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}  {self.id_number}"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class TrainerUnit(models.Model):
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trainer.name} -- {self.unit.unit_name}"


class TeachingAttendance(models.Model):
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    roll = models.CharField(max_length=20, null=True)
    is_clocked_in = models.BooleanField(default=True)
    is_clocked_out = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-clock_in", "-clock_out"]

    def __str__(self):
        return f"{self.unit.unit_name} {self.clock_in.astimezone()}"

    def save(self, *args, **kwargs):
        if self.clock_in and self.clock_out:
            # Ensure both clock_in and clock_out are timezone-aware
            if is_naive(self.clock_in):
                self.clock_in = make_aware(self.clock_in)
            if is_naive(self.clock_out):
                self.clock_out = make_aware(self.clock_out)

            # Now perform the subtraction safely
            time_diff = self.clock_out - self.clock_in
            self.time_taken = int(time_diff.total_seconds() // 60)  # Time in minutes
            self.is_clocked_out = True

        super().save(*args, **kwargs)


class WeekProgress(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)
    expected_hours = models.PositiveIntegerField(null=True)
    done_hours = models.PositiveIntegerField(null=True)
    percentage = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Week from {self.start_date} to {self.end_date}"
    
    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = datetime.now().date()
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=4)  # Assuming the week ends on Friday
        if self.expected_hours and self.done_hours:
            self.percentage = (self.done_hours / self.expected_hours) * 100
        super().save(*args, **kwargs)
