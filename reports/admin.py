from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Series)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(StudentExam)
admin.site.register(Mark)
admin.site.register(CourseUnit)
admin.site.register(StudentSeries)