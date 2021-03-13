from school.models import School
from curie.settings import SMS_API_KEY
from celery import shared_task
import requests
from sms.models import SMS
from students.models import Student
from staff.models import Staff
import urllib
from . constants import SMS_FAILED, SMS_SENT, SMS_PENDING


def get_sms_credentials():
    school = School.objects.first()
    if school:
        key = school.sms_api_key
        sender_id = school.sender_id or "CURIE"
        return key, sender_id
    return SMS_API_KEY, "CURIE"

@shared_task
def send_sms(numbers, message):
    SMS_API_KEY, sender_id = get_sms_credentials()
    for number in numbers:
        if not number:
            continue

        new_sms = SMS.objects.create(number=number, message=message)
        if len(number) != 10:
            new_sms.res_message = "Wrong number length."
            new_sms.status = SMS_FAILED
            new_sms.save()
            continue
    
        url = "https://sms.arkesel.com/sms/api?" + urllib.parse.urlencode(
                        {
                            "action":"send-sms", 
                            "api_key":SMS_API_KEY, 
                            "to":number, 
                            'from':sender_id,
                            "sms":message, 
                        }
                    )
        try:
            response = requests.get(url)
            if response.status_code == 200:  
                response = response.json()
                if response.get("code") == "ok":
                    SMS.objects.filter(id=new_sms.id).update(status=SMS_SENT, 
                                    res_code=response.get("code"), 
                                    res_message=response.get("message")
                    )
                else:
                    SMS.objects.filter(id=new_sms.id).update(status=SMS_FAILED, 
                                    res_code=response.get("code"), 
                                    res_message=response.get("message")
                    )
            else:
                SMS.objects.filter(id=new_sms.id).update(status=SMS_FAILED)
        except ConnectionError as e:
            SMS.objects.filter(id=new_sms.id).update(status=SMS_FAILED)

@shared_task
def sms_student_credentials():
    students = Student.objects.filter(completed=False)
    for student in students:
        message = f"Hello {student.get_full_name().upper()},\nUse these credentials to log in.\nUsername: {student.student_id}\nPin: {student.temporal_pin}\nGoto https://idealms.herokuapp.com/accounts/login/ to log in."
        # send_sms([student.sms_number], message)
        print(message)
            
@shared_task
def sms_staff_credentials():
    staffs = Staff.objects.filter(has_left=False)
    for staff in staffs:
        message = f"Hello {staff.get_full_name().upper()},\nUse these credentials to log in.\nUsername: {staff.staff_id}\nPin: {staff.temporal_pin}\nGoto https://idealms.herokuapp.com/accounts/login/ to log in."
        # send_sms([staff.sms_number], message)
        print(message)


@shared_task
def resend_sms(sms_id):
    print("Break")
    return
    sms = SMS.objects.get(id=sms_id)
    SMS_API_KEY, sender_id = get_sms_credentials()
    url = "https://sms.arkesel.com/sms/api?" + urllib.parse.urlencode(
                        {
                            "action":"send-sms", 
                            "api_key":SMS_API_KEY, 
                            "to":sms.number, 
                            'from':sender_id,
                            "sms":sms.message, 
                        }
                    )
    try:
        response = requests.get(url)
        if response.status_code == 200:  
            response = response.json()
            if response.get("code") == "ok":
                SMS.objects.filter(id=sms.id).update(status=SMS_SENT, 
                                res_code=response.get("code"), 
                                res_message=response.get("message")
                )
    except ConnectionError as e:
        pass


@shared_task
def send_all_failed_sms():
    failed_sms = SMS.objects.filter(status=SMS_FAILED)
    for sms in failed_sms:
        resend_sms(sms.id)

