# from sms.tasks import send_sms
# from students.models import Student
# from staff.models import Staff

# def sms_student_credentials(temporal_pin, number, student_id):

    
#     student = Student.objects.get(student_id=student_id)
#     message = f"""Hello {student.get_full_name().upper()},
#                             \nYour login details are:
#                             \nUsername: {student_id}
#                             \nPin: {temporal_pin}
#                             \nhttps://idealms.herokuapp.com/accounts/login/
#                             """
#     send_sms([number], message)
#     print("sms_student_credentials: ", temporal_pin, number, student_id)


# def sms_staff_credentials(temporal_pin, number, staff_id):
#     staff = Staff.objects.get(staff_id=staff_id)
#     message = f"""Hello {staff.get_full_name().upper()},
#                             \nYour login details are:
#                             \nUsername: {staff_id}
#                             \nPin: {temporal_pin}
#                             \nhttps://idealms.herokuapp.com/accounts/login/
#                             """
#     send_sms([number], message)
#     print("sms_staff_credentials: ", temporal_pin, number, staff_id)
