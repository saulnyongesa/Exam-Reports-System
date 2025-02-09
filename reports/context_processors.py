from datetime import datetime
from .models import *
from django.utils.deprecation import MiddlewareMixin
from django.db.models import Exists, OuterRef


def remaining_days(request):
    if request.user.is_authenticated:
        try:
            series = Series.objects.get(is_active=True)
            today = datetime.today().date()
            end_date = series.end_date
            remaining = abs((end_date - today).days)
            return {"remaining": remaining}
        except Series.DoesNotExist:
            return {"remaining": 0}
    else:
        return {"remaining": 0}


def unit_count(request):
    if request.user.is_authenticated:
        return {"unit_count": Unit.objects.count()}
    else:
        return {"unit_count": 0}


def student_count(request):
    if request.user.is_authenticated:
        return {"student_count": StudentExam.objects.count()}
    else:
        return {"student_count": 0}


def course_count(request):
    if request.user.is_authenticated:
        return {"course_count": Course.objects.count()}
    else:
        return {"course_count": 0}


class CheckSeriesDateMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            series = Series.objects.get(is_active=True)
            today = datetime.today().date()
            end_date = series.end_date
            if today > end_date:
                series.is_active = False
                series.save()
        except Series.DoesNotExist:
            series = Series.objects.filter(is_active=False)
            today = datetime.today().date()
            for series in series:
                end_date = series.end_date
                if today < end_date or today == end_date:
                    series.is_active = True
                    series.save()
        return None

class EnrollStudentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                active_series = Series.objects.get(is_active=True)
                unenrolled_students = StudentExam.objects.annotate(
                    enrolled=Exists(StudentSeries.objects.filter(
                        student=OuterRef('id'), 
                        series=active_series
                    ))
                ).filter(enrolled=False)
                StudentSeries.objects.bulk_create([
                    StudentSeries(student=student, series=active_series) 
                    for student in unenrolled_students
                ])
            except Series.DoesNotExist:
                pass
        return None

