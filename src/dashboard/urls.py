from django.urls import path

from . import views

# yapf: disable

app_name = "dashboard"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('delete/<str:model_name>/<str:instance_id>', views.DeleteModelView.as_view(), name='delete_model'),

    # Students
    path('students/', views.StudentsView.as_view(), name='students'),
    path('students/create-update', views.CreateUpdateStudentView.as_view(), name='create_update_student'),
    path('students/create-update-bulk', views.AddBulkStudents.as_view(), name='create_update_student_bulk'),

    # Subjects
    path('subjects/', views.SubjectsView.as_view(), name='subjects'),
    path('subjects/create-update', views.CreateUpdateSubjectView.as_view(), name="create_update_subject"),

    # Courses
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('courses/create-update', views.CreateUpdateCourseView.as_view(), name="create_update_course"),

    # Department
    path('departments/', views.DepartmentsView.as_view(), name='departments'),
    path('departments/create-update', views.CreateUpdateDepartmentView.as_view(), name="create_update_department"),

    # Staff
    path('staff/', views.StaffView.as_view(), name='staff'),
    path('staff/create-update', views.CreateUpdateStaffView.as_view(), name="create_update_staff"),

    # Staff
    path('classes/', views.ClassesView.as_view(), name='classes'),
    path('classes/create-update', views.CreateUpdateClassView.as_view(), name="create_update_class"),

    # House
    path('houses/', views.HousesView.as_view(), name='houses'),
    path('houses/create-update', views.CreateUpdateHouseView.as_view(), name="create_update_house"),

    # Action Center
    path('action-center/', views.ActionCenterView.as_view(), name='action_center'),
    path('action-center/subject-mapping', views.SubjectMappingView.as_view(), name='subject_mapping'),
    path('action-center/student-promotion', views.StudentPromotionView.as_view(), name='student_promotion'),
    path('action-center/academic-record-selection', views.AcademicRecordSelectionView.as_view(), name='academic_record_selection'),
    path('action-center/academic-record-data', views.AcademicRecordDataView.as_view(), name='academic_record_data'),

    # Reporting
    path('reporting/index', views.ReportingIndexView.as_view(), name='reporting_index'),

]
