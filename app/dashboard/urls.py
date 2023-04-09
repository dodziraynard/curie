from django.urls import path

from . import views

# yapf: disable

app_name = "dashboard"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('delete/<str:model_name>/<str:instance_id>', views.DeleteModelView.as_view(), name='delete_model'),
    path('model_agnostic_image_upload/<str:model_name>/<str:model_id>/<str:field_name>', views.ModelAgnosticImageUploadView.as_view(), name='model_agnostic_image_upload'),
    path('crop-model-image/<str:model_name>/<str:model_id>/<str:field_name>', views.CropModelImageView.as_view(), name='crop_model_image'),


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
    path('action-center/student-promotion-revert', views.RevertPromotionView.as_view(), name='student_promotion_revert'),
    path('action-center/academic-record-selection', views.AcademicRecordSelectionView.as_view(), name='academic_record_selection'),
    path('action-center/academic-record-data', views.AcademicRecordDataView.as_view(), name='academic_record_data'),

    # Reporting
    path('reporting/index', views.ReportingIndexView.as_view(), name='reporting_index'),
    path('reporting/student-full-report', views.StudentFullReportView.as_view(), name='student_full_report'),

    # Class teacher reporting
    path('reporting/class-teacher-report-filter', views.ClassTeacherSessionReportFilterView.as_view(), name='class_teacher_report_filter'),
    path('reporting/class-teacher-report-data', views.ClassTeacherSessionReportDataView.as_view(), name='class_teacher_report_data'),

    # House master reporting
    path('reporting/house-master-report-filter', views.HouseMasterSessionReportFilterView.as_view(), name='house_master_report_filter'),
    path('reporting/house-master-report-data', views.HouseMasterSessionReportDataView.as_view(), name='house_master_report_data'),

    # House master reporting
    path('reporting/assistant-head-report-filter', views.AssistantHeadSessionReportFilterView.as_view(), name='assistant_head_report_filter'),
    path('reporting/assistant-head-report-data', views.AssistantHeadSessionReportDataView.as_view(), name='assistant_head_report_data'),

    # Notifications
    path('notifications/', views.NotificationIndexView.as_view(), name='notifications'),
    path('notifications/history', views.NotificationHistoryView.as_view(), name='notification_history'),
    path('notifications/compose-sms/', views.ComposeSMS.as_view(), name='compose_sms'),
    path('notifications/preview-sms/', views.PreviewSMS.as_view(), name='preview_sms'),
    path('notifications/send-pin-sms/', views.SendPINNotification.as_view(), name='send_pin_sms'),
    path('notifications/confirm-pin-notification/', views.ConfirmPINNotification.as_view(), name='confirm_pin_notification'),

    path('notifications/report-notifications/', views.SendReportNotification.as_view(), name='report_notifications'),
    path('notifications/report-notification-confirmation/', views.ConfirmReportNotification.as_view(), name='report_notification_confirmation'),
]


urlpatterns += [
    path('accounting/', views.AccountingIndexView.as_view(), name='accounting'),
    path('accounting/invoices', views.InvoicesView.as_view(), name='invoices'),
    path('accounting/payments', views.PaymentsView.as_view(), name='payments'),
    path('accounting/create-update-payment/<str:student_id>/pay', views.CreateUpdatePayments.as_view(), name='create_update_payment'),
    path('accounting/create-update-invoice', views.CreateUpdateInvoiceView.as_view(), name='create_update_invoice'),
    path('accounting/invoice/<str:invoice_id>/create_update_invoice_item', views.CreateUpdateInvoiceItem.as_view(), name='create_update_invoice_item'),
    path('accounting/invoice/<str:invoice_id>/details', views.InvoiceDetailsView.as_view(), name='invoice_details'),
]