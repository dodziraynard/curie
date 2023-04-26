# Generated by Django 4.1.7 on 2023-04-26 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_alter_setupperms_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setupperms',
            options={'default_permissions': (), 'managed': False, 'permissions': [('manage_setup', 'Can manage system setup'), ('manage_users', 'Can manage system users'), ('view_dashboard', 'Can view dashboard'), ('manage_other_report', 'Can manage reports others'), ('manage_roles', 'Can manage roles'), ('view_action_center', 'Can view action center'), ('manage_action_center', 'Can manage action center'), ('add_subject_mapping', 'Can add subject mapping'), ('view_subject_mapping', 'Can view subject mapping'), ('view_promotion', 'Can view promotion'), ('add_promotion', 'Can add promotion'), ('revert_promotion', 'Can revert promotion'), ('change_class_teacher_remark', 'Can change class teacher remark'), ('change_house_master_remark', 'Can change house master remark'), ('append_signature', 'Can append signature to reports'), ('change_academic_record', 'Can change academic records'), ('view_student', 'Can view student'), ('add_student', 'Can add student'), ('change_student', 'Can change student'), ('delete_student', 'Can delete student'), ('view_staff', 'Can view staff'), ('add_staff', 'Can add staff'), ('change_staff', 'Can change staff'), ('delete_staff', 'Can delete staff'), ('view_class', 'Can view class'), ('add_class', 'Can add class'), ('change_class', 'Can change class'), ('delete_class', 'Can delete class'), ('view_subject', 'Can view subject'), ('add_subject', 'Can add subject'), ('change_subject', 'Can change subject'), ('delete_subject', 'Can delete subject'), ('view_department', 'Can view department'), ('add_department', 'Can add department'), ('change_department', 'Can change department'), ('delete_department', 'Can delete department'), ('view_house', 'Can view house'), ('add_house', 'Can add house'), ('change_house', 'Can change house'), ('delete_house', 'Can delete house'), ('view_accounting', 'Can access accounting menu'), ('view_invoice', 'Can view invoice'), ('add_invoice', 'Can add invoice'), ('change_invoice', 'Can change invoice'), ('apply_invoice', 'Can apply invoice'), ('delete_invoice', 'Can delete invoice'), ('view_invoiceitem', 'Can view invoice item'), ('add_invoiceitem', 'Can add invoice item'), ('change_invoiceitem', 'Can change invoice item'), ('delete_invoiceitem', 'Can delete invoice item'), ('view_payment', 'Can view payment item'), ('add_payment', 'Can add payment item'), ('change_payment', 'Can change payment item'), ('delete_payment', 'Can delete payment item'), ('view_alert', 'Can access alert menu'), ('compose_sms', 'Can compose sms'), ('send_pin_notification', 'Can send pin notification'), ('send_report_notification', 'Can send report notification'), ('resend_notification', 'Can ressend notifications'), ('view_notification_history', 'Can view notification history'), ('view_reporting', 'Can access reporting menu'), ('generate_limited_report', 'Can access reporting menu')]},
        ),
    ]
