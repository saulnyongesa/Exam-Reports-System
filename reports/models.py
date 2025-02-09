from django.db import models


# Create your models here.
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
    course_name = models.CharField(max_length=200, null=True)
    course_code = models.CharField(max_length=20, null=True, unique=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.course_name


class Unit(models.Model):
    unit_name = models.CharField(max_length=200, null=True)
    unit_code = models.CharField(max_length=20, null=True, unique=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.unit_name


class CourseUnit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not CourseUnit.objects.filter(course=self.course, unit=self.unit).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.course_name}: UNIT: {self.unit.unit_name}"


class StudentExam(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
