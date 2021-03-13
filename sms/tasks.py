from school.models import School
from curie.settings import SMS_API_KEY
from celery import shared_task
import requests


def get_sms_credentials():
    school = School.objects.first()
    if school:
        key = school.sms_api_key
        sender_id = school.sender_id or "CURIE LMS"
        return key, sender_id
    return SMS_API_KEY, "CURIE LMS"


@shared_task
def send_sms(numbers, message):
    SMS_API_KEY, sender_id = get_sms_credentials()
    for number in numbers:
        url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key={SMS_API_KEY}&to={number}&from={sender_id}&sms={message}"
        try:
            # response = requests.get(url)
            pass
        except ConnectionError as e:
            print(response)
