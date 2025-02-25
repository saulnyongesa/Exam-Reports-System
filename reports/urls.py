from django.urls import path
from . import views, excel


urlpatterns = [
    path('profile/', views.profile, name='report-profile-url'),
    path('Profile/Edit/', views.profile_edit, name='report-profile-edit-url'),
   
    
    
    path('', views.report_home, name='report-home-url'),
    path('students/', views.students_all, name='report-students-all-url'),
    path('student/<int:student_id>/', views.student_detail, name='report-student-detail-url'),
    path('student/<int:student_id>/edit/', views.edit_student, name='report-edit-student-url'),
    path('student/<int:student_id>/delete/', views.delete_student, name='report-delete-student-url'),
    path('add_student/', views.add_student, name='report-add-student-url'),
    
    
    path('mark_entry/', views.mark_entry, name='report-mark-entry-url'),
    path('student/search/', views.search, name='report-search-url'),
    path('mark/enter/<int:id>/', views.mark_add, name='report-add-mark-url'),
    path('mark/edit/<int:id>/', views.marks_edit, name='report-edit-mark-url'),
    path('student/mark/add/<str:id>/', views.mark_add_after_student_add, name='report-mark-add-after-student-add-url'),



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

    path('import_students/', views.import_students_from_excel, name='report-import-students-url'),
    
]