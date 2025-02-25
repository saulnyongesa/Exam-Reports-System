from datetime import datetime, date
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
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
def dashboard(request):
    if request.user.is_authenticated:
        num_trainers = Trainer.objects.count()
        num_students = StudentExam.objects.count()
        num_units = Unit.objects.count()
        num_courses = Course.objects.count()
        num_admins = User.objects.filter(is_staff=True).count()
        classes_today = TeachingAttendance.objects.filter(clock_out=date.today()).count()
        return {
            "num_trainers": num_trainers,
            "num_students": num_students,
            "num_units": num_units,
            "num_courses": num_courses,
            "num_admins": num_admins if not request.user else num_admins - 1,
            "classes_today": classes_today,
        }
    else:
        return {
            "num_trainers": 0,
            "num_students": 0,
            "num_units": 0,
            "num_courses": 0,
            "num_admins": 0,
            "classes_today": 0,
        }

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


class DesktopOnlyMiddleware:
    MOBILE_USER_AGENTS = [
        "Mobile", "Android", "iPhone", "iPad", "iPod", "BlackBerry", "Opera Mini", "IEMobile"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # If the request comes from a mobile device, deny access
        if any(mobile in user_agent for mobile in self.MOBILE_USER_AGENTS):
            return HttpResponseForbidden("Access restricted to desktop users only.")

        return self.get_response(request)

class CheckOTPTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        otps = OTP.objects.filter(is_used=False)
        for otp in otps:
            expire_time = otp.expire_time
            if expire_time <= timezone.now():
                otp.is_used = True
                otp.save()
                otp.delete()
        return None

class RestrictUserFromAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_examination_officer and request.path.startswith('/admin/'):
            return redirect('/report/')  # Redirect teachers to app
        if request.user.is_authenticated and request.user.is_superuser and request.path.startswith('/report/'):
            return redirect('/base/')  # Redirect teachers to app

        return self.get_response(request)