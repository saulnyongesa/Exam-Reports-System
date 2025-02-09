from io import BytesIO
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib import messages
from openpyxl import load_workbook
from reports.forms import *
from reports.models import *
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
import csv
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import modelformset_factory
from .forms import MarksFormSet  # Import the formset


# Create your views here.
def report_home(request):
    series = None
    try:
        series = Series.objects.get(is_active=True)
    except Series.DoesNotExist:
        pass
    context = {"series": series}
    return render(request, "reports/home.html", context)


def students_all(request):
    students = StudentExam.objects.filter(is_active=True)
    return render(request, "reports/students.html", {"students": students})


def student_detail(request, student_id):
    student = get_object_or_404(StudentExam, id=student_id)
    return render(request, "reports/student_details.html", {"student": student})


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("report-students-all-url")
    else:
        form = StudentForm()
    return render(request, "reports/student_add.html", {"form": form})


def edit_student(request, student_id):
    student = get_object_or_404(StudentExam, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("report-students-all-url")
    else:
        form = StudentForm(instance=student)
    return render(request, "reports/student_edit.html", {"form": form})


def delete_student(request, student_id):
    student = get_object_or_404(StudentExam, id=student_id)
    if request.method == "DELETE":
        student.delete()
        return JsonResponse(
            {"success": True, "message": "Student deleted successfully"}
        )
    return JsonResponse({"success": False, "message": "Failed to delete student"})


def courses_all(request):
    courses = Course.objects.all()
    return render(request, "reports/courses.html", {"courses": courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "reports/course_details.html", {"course": course})


def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("report-courses-all-url")
    else:
        form = CourseForm()
    return render(request, "reports/course_add.html", {"form": form})


def edit_course(request, course_id):
    form = CourseForm(request.POST)
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("report-courses-all-url")
    else:
        form = CourseForm(instance=course)
    return render(request, "reports/course_edit.html", {"form": form})


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "DELETE":
        course.delete()
        return JsonResponse({"success": True, "message": "Course deleted successfully"})
    return JsonResponse({"success": False, "message": "Failed to delete course"})


def units_all(request):
    units = Unit.objects.all()
    return render(request, "reports/units.html", {"units": units})


def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    return render(request, "reports/unit_details.html", {"unit": unit})


def add_unit(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("report-units-all-url")
    else:
        form = UnitForm()
    return render(request, "reports/unit_add.html", {"form": form})


def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect("report-units-all-url")
    else:
        form = UnitForm(instance=unit)
    return render(request, "reports/unit_edit.html", {"form": form})


def delete_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.method == "DELETE":
        unit.delete()
        return JsonResponse({"success": True, "message": "Unit deleted successfully"})
    return JsonResponse({"success": False, "message": "Failed to delete unit"})


def mark_entry(request):
    return render(request, "reports/mark_entry.html")


def search(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query", "")
        students = StudentExam.objects.filter(registration_number__icontains=query)
        results = [
            {
                "id": student.id,
                "name": f"{student.first_name} {student.second_name} {student.last_name}",
                "regno": student.registration_number,
            }
            for student in students
        ]
        return JsonResponse({"success": True, "data": results})
    return JsonResponse({"success": False, "message": "Invalid request method"})


def mark_add(request, id):
    student = get_object_or_404(StudentExam, id=id)
    try:
        series = Series.objects.get(is_active=True)
    except Series.DoesNotExist:
        messages.error(request, "No active Series, Please Create One or Extend the current Series End Dates")
        return redirect("report-series-url")
    units = CourseUnit.objects.filter(course=student.course)
    marks = Mark.objects.filter(student=student, series=series)
    # Check if marks already exist for this student
    if marks.exists():
        messages.error(request, "Marks already entered for this student.")
        return HttpResponseRedirect("/report/mark/edit/" + str(id) + "/")

    if request.method == "POST":
        marks_to_save = []
        for unit in units:
            cat_mark = request.POST.get(f"cat_mark_{unit.unit.id}")
            exam_mark = request.POST.get(f"exam_mark_{unit.unit.id}")
            project_mark = request.POST.get(f"project_mark_{unit.unit.id}")

            if cat_mark and exam_mark and project_mark:  # Ensure values are not empty
                mark = Mark(
                    student=student,
                    series=series,
                    unit=unit.unit,
                    cat_mark=int(cat_mark),
                    exam_mark=int(exam_mark),
                    project_mark=int(project_mark),
                )
                marks_to_save.append(mark)

        if marks_to_save:
            Mark.objects.bulk_create(marks_to_save)  # Save all marks at once
            messages.success(request, "Marks saved successfully.")
            return redirect(
                "report-mark-entry-url"
            )  # Change this to your redirect page
        else:
            messages.error(request, "Please enter all required marks.")

    context = {
        "student": student,
        "units": units,
        "series": series,
    }
    return render(request, "reports/marks_add.html", context)


def marks_edit(request, id):
    student = get_object_or_404(StudentExam, id=id)
    units = CourseUnit.objects.filter(course=student.course)
    series = Series.objects.get(is_active=True)

    # Retrieve marks as a dictionary {unit.id: mark object}
    marks = {
        mark.unit.id: mark
        for mark in Mark.objects.filter(student=student, series=series)
    }

    if request.method == "POST":
        for unit in units:
            cat_mark = request.POST.get(f"cat_mark_{unit.unit.id}")
            exam_mark = request.POST.get(f"exam_mark_{unit.unit.id}")
            project_mark = request.POST.get(f"project_mark_{unit.unit.id}")

            if unit.unit.id in marks:
                # Update existing marks
                mark = marks[unit.unit.id]
                mark.cat_mark = cat_mark
                mark.exam_mark = exam_mark
                mark.project_mark = project_mark
                mark.save()
            else:
                # Create a new mark entry if not present
                Mark.objects.create(
                    student=student,
                    series=series,
                    unit=unit.unit,
                    cat_mark=cat_mark,
                    exam_mark=exam_mark,
                    project_mark=project_mark,
                )

        messages.success(request, "Marks updated successfully!")
        return redirect(
            "report-mark-entry-url"
        )  # Redirect to prevent duplicate form submission

    context = {
        "student": student,
        "units": units,
        "series": series,
        "marks": marks,  # Pass as a dictionary
    }
    return render(request, "reports/marks_edit.html", context)


def marks_reports(request):
    series = Series.objects.all
    units = Unit.objects.all
    courses = Course.objects.all
    students = StudentExam.objects.all
    context = {"series": series, "units": units, "courses": courses, "students": students}
    return render(request, "reports/marks_report.html", context)


def series_view(request):
    series = Series.objects.all()
    context = {"serieses": series}
    return render(request, "reports/series.html", context)


def add_series(request):
    if request.method == "POST":
        form = SeriesAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("report-series-url")
    else:
        form = SeriesAddForm()
    return render(request, "reports/series_add.html", {"form": form})


def edit_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    if request.method == "POST":
        form = SeriesAddForm(request.POST, instance=series)
        if form.is_valid():
            form.save()
            return redirect("report-series-url")
    else:
        form = SeriesAddForm(instance=series)
    return render(request, "reports/series_edit.html", {"form": form})


def delete_series(request, series_id):
    series = get_object_or_404(Series, id=series_id, is_active=True)
    if request.method == "DELETE":
        series.delete()
        return JsonResponse({"success": True, "message": "Series deleted successfully"})
    return JsonResponse({"success": False, "message": "Failed to delete Series"})


def import_units_from_excel(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authenticated to perform this action")
        return redirect("report-home-url")

    if request.method == "POST" and request.FILES.get("file"):
        excel_file = request.FILES["file"]
        wb = load_workbook(filename=BytesIO(excel_file.read()))
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):  # Skip row 1 (titles)
            row_values = list(row)
            if len(row_values) < 2 or not all(row_values):  
                continue  # Skip rows with missing values

            unit_name, unit_code = row_values[:2]

            if not Unit.objects.filter(unit_code=unit_code).exists():
                Unit.objects.create(unit_name=unit_name, unit_code=unit_code)

        messages.success(request, "Units imported successfully")
        return redirect("report-units-all-url")

    return render(request, "reports/import_units.html")


def import_courses_from_excel(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authenticated to perform this action")
        return redirect("report-home-url")

    if request.method == "POST" and request.FILES.get("file"):
        excel_file = request.FILES["file"]
        wb = load_workbook(filename=BytesIO(excel_file.read()))
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):  # Skip row 1 (titles)
            row_values = list(row)
            if len(row_values) < 2 or not all(row_values):  
                continue  # Skip rows with missing values

            course_name, course_code = row_values[:2]

            if not Course.objects.filter(course_code=course_code).exists():
                Course.objects.create(course_name=course_name, course_code=course_code)

        messages.success(request, "Courses imported successfully")
        return redirect("report-courses-all-url")

    return render(request, "reports/import_courses.html")


def import_students_from_excel(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authenticated to perform this action")
        return redirect("report-home-url")

    if request.method == "POST" and request.FILES.get("file"):
        excel_file = request.FILES["file"]
        wb = load_workbook(filename=BytesIO(excel_file.read()))
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):
            row_values = list(row)  # Convert to list
            if len(row_values) < 7:  
                continue  # Skip rows with missing values
            
            first_name, second_name, last_name, registration_number, email, phone, course_code = row_values[:7]  

            if not registration_number or not course_code:
                continue  # Skip invalid rows
            
            course = Course.objects.filter(course_code=course_code).first()
            if course and not StudentExam.objects.filter(registration_number=registration_number).exists():
                StudentExam.objects.create(
                    first_name=first_name,
                    second_name=second_name,
                    last_name=last_name,
                    registration_number=registration_number,
                    email=email,
                    phone=phone,
                    course=course
                )

        messages.success(request, "Students imported successfully")
        return redirect("report-students-all-url")

    return render(request, "reports/import_students.html")



def course_units_view(request):
    courses = Course.objects.all
    course_units = CourseUnit.objects.all()
    units = Unit.objects.all()
    context = {
        'courses': courses,
        "course_units": course_units,
        'units': units
    }
    return render(request, 'reports/courses_units.html', context)

def get_unlinked_units(request, course_id):
    linked_units = CourseUnit.objects.filter(course_id=course_id).values_list('unit_id', flat=True)
    unlinked_units = Unit.objects.exclude(id__in=linked_units)
    return JsonResponse({
        "units": list(unlinked_units.values('id', 'unit_name', 'unit_code'))
    })
    
@csrf_exempt
def save_course_units(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            course_id = data.get("course_id")
            unit_ids = data.get("units", [])
            
            # Get the course instance
            course = get_object_or_404(Course, id=course_id)
            
            # Link the selected units to the course
            for unit_id in unit_ids:
                unit = get_object_or_404(Unit, id=unit_id)
                # Create a CourseUnit relationship
                CourseUnit.objects.get_or_create(course=course, unit=unit)
            
            return JsonResponse({"success": True, "message": "Units saved successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

def delete_course_unit(request, id):
        try:
            course_unit = get_object_or_404(CourseUnit, id=id)
            course_unit.delete()
            return redirect("report-course-units-view-url")
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)