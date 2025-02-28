from django.urls import path
from base import views
from base import excel as admin_excel


urlpatterns = [
    path('', views.home, name='admin-home-url'),
    path('profile/', views.profile, name='admin-profile-url'),
    path('Profile/Edit/', views.profile_edit, name='admin-profile-edit-url'),
    path('admin/signout/', views.sign_out_user, name='admin-signout-url'),
    
    path('admins/', views.admins_all, name='admins-url'),
    path('admin_signup/', views.admin_signup, name='admin-signup-url'),
    path('admin_delete/<int:admin_id>/', views.admin_delete, name='admin-delete-url'),
    path('admin/<int:admin_id>/', views.admin_status, name='admin-status-url'),
    
    path('trainers/', views.trainers_all, name='trainers-url'),
    path('trainer_signup/', views.trainer_signup, name='trainer-signup-url'),
    path('trainer_delete/<int:trainer_id>/', views.trainer_delete, name='trainer-delete-url'),
    path('trainer/<int:trainer_id>/', views.trainer_status, name='trainer-status-url'),
    path('trainer/details/<int:trainer_id>/', views.trainer_details, name='trainer-url'),
    path('trainer/details/edit/<int:trainer_id>/', views.trainer_edit, name='trainer-edit-url'),
    path('trainer/unit/delete/<int:id>/', views.trainer_unit_delete, name='trainer-unit-delete-url'),
    path('trainer/get-unlinked-units/<int:trainer_id>/', views.get_unlinked_units_to_trainer, name='get_unlinked_units'),
    path('trainer/save-trainer-units/', views.save_trainer_units, name='save_trainer_units'),

    
    path('import_units/', views.import_units_from_excel, name='admin-import-units-url'),
    path('import_courses/', views.import_courses_from_excel, name='admin-import-courses-url'),
    
    path('courses/', views.courses_all, name='admin-courses-url'),
    path('course/<int:course_id>/', views.course_detail, name='admin-course-detail-url'),
    path('add_course/', views.add_course, name='admin-add-course-url'),
    path('course/<int:course_id>/edit/', views.edit_course, name='admin-edit-course-url'),
    path('course/<int:course_id>/delete/', views.delete_course, name='admin-delete-course-url'),
    
    path('units/', views.units_all, name='admin-units-url'),
    path('unit/<int:unit_id>/', views.unit_detail, name='admin-unit-detail-url'),
    path('add_unit/', views.add_unit, name='admin-add-unit-url'),
    path('unit/<int:unit_id>/edit/', views.edit_unit, name='admin-edit-unit-url'),
    path('unit/<int:unit_id>/delete/', views.delete_unit, name='admin-delete-unit-url'),
    
    path('course/units/view/', views.course_units_view, name='admin-course-units-url'),
    path('get-unlinked-units/<int:course_id>/', views.get_unlinked_units, name='admin-get-unlinked-units'),
    path('save-course-units/', views.save_course_units, name='admin-save-course-units'),
    path('delete-course-units/<int:id>/', views.delete_course_unit, name='admin-delete-course-units-url'),
    
    path('clockinout/', views.clock, name='admin-clock-url'),
    path('clockin/<trainer_id>/', views.clock_in, name='admin-clock-in-url'),
    path('clockout/<trainer_id>/', views.clock_out, name='admin-clock-out-url'),
    path('clock_in/unit_data/', views.get_unit_data, name='get-unit-data-url'),
    
    path('clock-reports/', views.clock_reports, name='clock-reports-url'),
    path('clock-reports/clock-history-triner/', views.clock_history_trainer, name='clock-history-trainer-url'),
    path('clock-reports/clock-history-all/', views.clock_history_all, name='clock-history-all-url'),
    path('clock-reports/active-classes/', views.active_classes, name='active-classes-url'),
    
    path('generate/excel/<trainer_id>', admin_excel.generate_excel_clock_history_trainer, name='generate-excel-clock-history-trainer-url'),
    path('generate/excel/all/', admin_excel.generate_excel_clock_history_all, name='generate-excel-clock-history-all-url'),

    
      
    path('export_excel/', admin_excel.generate_excel_for_student_reports, name='admin-export-excel-student-url'),
    path('export_excel_course/', admin_excel.generate_excel_for_course_reports, name='admin-export-excel-course-url'),
    path('export_excel_unit/', admin_excel.generate_excel_for_unit_reports, name='admin-export-excel-unit-url'),
    
    path('download/import_courses/template/', admin_excel.import_courses_template, name='admin-import-courses-template-url'),
    path('download/import_units/template/', admin_excel.import_units_template, name='admin-import-units-template-url'),
    path('download/import_students/template/', admin_excel.import_students_template, name='admin-import-students-template-url'),   
]