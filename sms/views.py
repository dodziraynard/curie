from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from students.models import Student
from staff.models import Staff
from .models import SMS
import requests
import urllib
from sms.tasks import (send_sms,
                        sms_student_credentials,
                        sms_staff_credentials,
                        resend_sms,
                        send_all_failed_sms)


class NewSMS(View):
    template_name = "sms/new_sms.html"
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request, **kwargs):
        numbers = request.POST.get("numbers")
        message = request.POST.get("message")
        numbers = numbers.replace(" ", '').split(",")
        # send_sms.delay(numbers, message)
        send_sms(numbers, message)
        request.session['message'] = "Messages queued successfully."
        return redirect("sms:new_sms")

class ForwardCredentials(View):
    template_name = 'sms/forward_credentials.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request, **kwargs):
        category = request.POST.get("category")
        if category == 'students':
            sms_student_credentials()

        elif category == 'staff':
            sms_staff_credentials()
        else:
            sms_student_credentials()
            sms_staff_credentials()

        return redirect("sms:forward_credentials")

class Balance(View):
    template_name = 'sms/balance.html'
    def get(self, request):
        key = request.school.sms_api_key
        url = "https://sms.arkesel.com/sms/api?" + urllib.parse.urlencode(
                        {
                            "action":"check-balance", 
                            "api_key":key, 
                            'response':'json'
                        }
                    )
        reponse = requests.get(url).json()
        context = {
            "balance":reponse.get("balance")
        }
        return render(request, self.template_name, context)

class Messages(View):
    template_name = 'sms/messages.html'
    def get(self, request):
        return render(request, self.template_name)

class ResendSMS(View):
    template_name = 'sms/messages.html'
    def get(self, request):
        sms_id = request.GET.get("sms_id")
        all_failed = request.GET.get("all_failed")
        
        if sms_id and SMS.objects.filter(id=sms_id).exists():
            resend_sms(sms_id)
        if all_failed:
            send_all_failed_sms()
        
        request.session['message'] = "Messages queued successfully."
        return redirect("sms:messages")