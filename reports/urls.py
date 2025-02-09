from django.urls import path
from . import views, excel

urlpatterns = [
    path('', views.report_home, name='report-home-url'),
    path('students/', views.students_all, name='report-students-all-url'),
    path('student/<int:student_id>/', views.student_detail, name='report-student-detail-url'),
    path('student/<int:student_id>/edit/', views.edit_student, name='report-edit-student-url'),
    path('student/<int:student_id>/delete/', views.delete_student, name='report-delete-student-url'),
    path('add_student/', views.add_student, name='report-add-student-url'),
    
    path('courses/', views.courses_all, name='report-courses-all-url'),
    path('course/<int:course_id>/', views.course_detail, name='report-course-detail-url'),
    path('add_course/', views.add_course, name='report-add-course-url'),
    path('course/<int:course_id>/edit/', views.edit_course, name='report-edit-course-url'),
    path('course/<int:course_id>/delete/', views.delete_course, name='report-delete-course-url'),
    
    path('units/', views.units_all, name='report-units-all-url'),
    path('unit/<int:unit_id>/', views.unit_detail, name='report-unit-detail-url'),
    path('add_unit/', views.add_unit, name='report-add-unit-url'),
    path('unit/<int:unit_id>/edit/', views.edit_unit, name='report-edit-unit-url'),
    path('unit/<int:unit_id>/delete/', views.delete_unit, name='report-delete-unit-url'),
    
    path('mark_entry/', views.mark_entry, name='report-mark-entry-url'),
    path('student/search/', views.search, name='report-search-url'),
    path('mark/enter/<int:id>/', views.mark_add, name='report-add-mark-url'),
    path('mark/edit/<int:id>/', views.marks_edit, name='report-edit-mark-url'),
    
    path('course/units/view/', views.course_units_view, name='report-course-units-view-url'),
    path('get-unlinked-units/<int:course_id>/', views.get_unlinked_units, name='get-unlinked-units'),
    path('save-course-units/', views.save_course_units, name='save_course_units'),
    path('delete-course-units/<int:id>/', views.delete_course_unit, name='report-delete-course-units-url'),


    path('mark/report/', views.marks_reports, name='report-mark-reports-url'),
    
    
    path('export_excel/', excel.generate_excel_for_student_reports, name='report-export-excel-student-url'),
    path('export_excel_course/', excel.generate_excel_for_course_reports, name='report-export-excel-course-url'),
    path('export_excel_unit/', excel.generate_excel_for_unit_reports, name='report-export-excel-unit-url'),
    
    path('series/', views.series_view, name='report-series-url'),
    path('series/add/', views.add_series, name='report-add-series-url'),
    path('series/<int:series_id>/edit/', views.edit_series, name='report-edit-series-url'),
    path('series/<int:series_id>/delete/', views.delete_series, name='report-delete-series-url'),
    
    path('export_excel_marks/series/<int:series_id>/', excel.generate_excel_for_marks_per_series_reports, name='report-export-excel-marks-url'),
    path('export_excel_marks/unit/<int:series_id>/<int:unit_id>/', excel.generate_excel_for_marks_per_unit_reports, name='report-export-excel-marks-url'),
    path('export_excel_marks/course/<int:series_id>/<int:course_id>/', excel.generate_excel_for_marks_per_course_reports, name='report-export-excel-marks-url'),
    path('export_excel_marks/student/<int:series_id>/<int:student_id>/', excel.generate_excel_for_marks_per_student_reports, name='report-export-excel-marks-url'),
    
    path('import_units/', views.import_units_from_excel, name='report-import-units-url'),
    path('import_courses/', views.import_courses_from_excel, name='report-import-courses-url'),
    path('import_students/', views.import_students_from_excel, name='report-import-students-url'),
    
    path('download/import_courses/template/', excel.import_couses_template, name='report-import-courses-template-url'),
    path('download/import_units/template/', excel.import_units_template, name='report-import-units-template-url'),
    path('download/import_students/template/', excel.import_students_template, name='report-import-students-template-url'),

]