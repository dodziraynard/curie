from django.urls import path

from . import views

# yapf: disable

app_name = "dashboard"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('delete/<str:model_name>/<str:instance_id>', views.DeleteModelView.as_view(), name='delete_model'),
    path('model_agnostic_image_upload/<str:model_name>/<str:model_id>/<str:field_name>', views.ModelAgnosticImageUploadView.as_view(), name='model_agnostic_image_upload'),
    path('crop-model-image/<str:model_name>/<str:model_id>/<str:field_name>', views.CropModelImageView.as_view(), name='crop_model_image'),
    path('tasks/<str:task_id>/stream-status', views.StreamTaskStatusView.as_view(), name='stream_task_status'),

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

    # House
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('tasks/create-update', views.CreateUpdateTaskView.as_view(), name="create_update_task"),
    path('tasks/task-send-notification', views.SendTaskNotification.as_view(), name="task_send_notification"),

    # Action Center
    path('action-center/', views.ActionCenterView.as_view(), name='action_center'),
    path('action-center/subject-mapping', views.SubjectMappingView.as_view(), name='subject_mapping'),
    path('action-center/reset-subject-mapping', views.ResetSubjectMappingView.as_view(), name='reset_subject_mapping'),
    path('action-center/student-promotion', views.StudentPromotionView.as_view(), name='student_promotion'),
    path('action-center/student-promotion-revert', views.RevertPromotionView.as_view(), name='student_promotion_revert'),
    path('action-center/academic-record-selection', views.AcademicRecordSelectionView.as_view(), name='academic_record_selection'),
    path('action-center/academic-record-data', views.AcademicRecordDataView.as_view(), name='academic_record_data'),
    path('action-center/reset-academic-record-data', views.ResetAcademicRecord.as_view(), name='reset_academic_record_data'),

    # Reporting
    path('reporting/index', views.ReportingIndexView.as_view(), name='reporting_index'),
    path('reporting/student-full-report', views.StudentFullReportView.as_view(), name='student_full_report'),
    path('reporting/generate-report-sheet', views.BulkAcademicRecordReportView.as_view(), name='gerate_bulk_student_report_sheet'),
    path('reporting/generate-report-sheet/<str:task_id>/<str:filename>/status', views.StudentReportGenerationStatusView.as_view(), name='bulk_report_sheet_generation_status'),

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
    path('notifications/bill-notifications/', views.SendBillNotification.as_view(), name='bill_notifications'),
    path('notifications/report-notification-confirmation/', views.ConfirmReportNotification.as_view(), name='report_notification_confirmation'),
    path('notifications/bill-notification-confirmation/', views.ConfirmBillNotification.as_view(), name='bill_notification_confirmation'),
]


urlpatterns += [
    path('accounting/', views.AccountingIndexView.as_view(), name='accounting'),
    path('accounting/invoices', views.InvoicesView.as_view(), name='invoices'),
    path('accounting/payments', views.PaymentsView.as_view(), name='payments'),
    path('accounting/create-update-payment/<str:student_id>/pay', views.CreateUpdatePayments.as_view(), name='create_update_payment'),
    path('accounting/create-update-invoice', views.CreateUpdateInvoiceView.as_view(), name='create_update_invoice'),
    path('accounting/invoice/<str:invoice_id>/create_update_invoice_item', views.CreateUpdateInvoiceItem.as_view(), name='create_update_invoice_item'),
    path('accounting/invoice/<str:invoice_id>/details', views.InvoiceDetailsView.as_view(), name='invoice_details'),
    
    path('accounting/generate-bill-sheet/<str:invoice_id>', views.BulkInvoiceGenerator.as_view(), name='gerate_bulk_student_bill_sheet'),
    path('accounting/generate-bill-sheet/<str:task_id>/<str:filename>/status', views.GeneralReportStatusView.as_view(), name='bulk_bill_sheet_generation_status'),
    
    path('accounting/student-invoices/<str:student_id>/', views.StudentInvoicesView.as_view(), name='student_invoices'),
    path('accounting/student-invoices/<str:student_id>/<str:invoice_id>', views.StudentInvoiceDetailView.as_view(), name='student_invoice_details'),
]

urlpatterns += [
    path('inventory/', views.InventoryIndexView.as_view(), name='inventory_index'),
    path('inventory/inventories', views.InventoriesView.as_view(), name='inventories'),
    path('inventory/inventories/create-update', views.CreateUpdateInventoryView.as_view(), name="create_update_inventory"),

    path('inventory/issuance', views.IssuanceView.as_view(), name='issuance'),
    path('inventory/issuance/create-update', views.CreateUpdateIssuanceView.as_view(), name="create_update_issuance"),
]

#Personal
urlpatterns += [
    path('personal/academic-record', views.PesonalAcademicRecord.as_view(), name='personal_academic_record'),
    path('personal/my-invoices', views.MyInvoicesView.as_view(), name='my_invoices'),
    path('personal/my-invoices/<str:invoice_id>/detail', views.MyInvoiceDetailView.as_view(), name='my_invoice_detail'),
    path('personal/payment-history', views.PersonalPaymentHistory.as_view(), name='payment_history'),
]

# User profile
urlpatterns += [
    path('user-profile', views.UserProfileIndexView.as_view(), name='user_profile'),
    path('user-profile/photo', views.UserProfilePhotoView.as_view(), name='user_profile_profile'),
]