import base64
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from accounts.models import Account
from accounts.models import User
from dashboard.models import Klass, Staff
from setup.models import School
from dashboard.models import Student

from lms.utils.functions import crop_image
from celery.result import AsyncResult
from django.http import StreamingHttpResponse


class IndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/index.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        user_ids = Account.objects.filter(
            main_balance__lt=0).order_by("main_balance").values_list(
                "user", flat=True)[:100]
        users = User.objects.filter(id__in=user_ids)
        students = Student.objects.filter(user__in=users)

        school = School.objects.first()
        class_count = Klass.objects.filter(deleted=False).count()
        student_count = Student.objects.filter(deleted=False).count()
        staff_count = Staff.objects.filter(deleted=False).count()
        user_count = User.objects.filter(deleted=False).count()
        context = {
            "students": students,
            "school": school,
            "class_count": class_count,
            "student_count": student_count,
            "staff_count": staff_count,
            "user_count": user_count,
        }
        return render(request, self.template_name, context)


class DeleteModelView(PermissionRequiredMixin, View):
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, model_name, instance_id):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, model_name, instance_id):
        # Get the model
        content_type = ContentType.objects.filter(model=model_name).first()
        if not content_type:
            raise PermissionDenied("Model not found")

        model_class = content_type.model_class()

        permission_name = f"{content_type.app_label}.delete_{model_name}"
        if not request.user.has_perm(permission_name):
            raise PermissionDenied()

        # Get the model instance
        res = None
        try:
            if hasattr(model_class, "deleted"):
                model_class.objects.filter(id=instance_id).update(deleted=True)
                messages.success(request, "Successfully deleted.")
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                res = model_class.objects.filter(id=instance_id).delete()
        except ProtectedError as _:
            messages.error(
                request,
                "This item is protected and cannot be deleted until all references are removed."
            )
            return redirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            messages.error(request, str(e))
            return redirect(request.META.get("HTTP_REFERER"))
        if res:
            messages.success(request, "Successfully deleted.")
        else:
            messages.info(request, "Item not found")

        return redirect(request.META.get("HTTP_REFERER"))


class ModelAgnosticImageUploadView(View):

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, model_name, model_id, field_name):
        image_data = request.POST.get('image')
        image_file = request.FILES.get('image')
        is_ajax = request.POST.get('is_ajax', False)

        # Get the model
        content_type = ContentType.objects.filter(model=model_name).first()
        if not content_type:
            if is_ajax:
                return JsonResponse({"message": "Record not found."})
            else:
                messages.error(request, "Record not found.")
                return redirect(request.META.get("HTTP_REFERER"))

        model_class = content_type.model_class()

        # Get the model instance
        model_instance = model_class.objects.filter(id=model_id).first()
        if not model_instance:
            if is_ajax:
                return JsonResponse({"message": "Record not found."})
            else:
                messages.error(request, "Record not found.")
                return redirect(request.META.get("HTTP_REFERER"))

        if image_data:
            image_format, imgstr = image_data.split(';base64,')
            ext = image_format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            myfile = "photo-" + time.strftime("%Y%m%d-%H%M%S") + "." + ext

            # Save photo
            getattr(model_instance, field_name).save(myfile, data)
            model_instance.save()
        elif image_file:
            # Save photo
            getattr(model_instance, field_name).save(image_file.name,
                                                     image_file)
            model_instance.save()

        messages.success(request, "Image updated successfully.")

        if is_ajax:
            return JsonResponse({
                "success": True,
                "message": "Image uploaded successfully.",
            })
        else:
            return redirect(request.META.get("HTTP_REFERER"))


class CropModelImageView(PermissionRequiredMixin, View):
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, *args, **kwargs):
        return redirect("dashboard:products")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, model_name, model_id, field_name):
        crop_data = request.POST.get("cropdata")

        # Get the model
        content_type = ContentType.objects.filter(model=model_name).first()
        if not content_type:
            messages.error(request, "Record not found.")
            return redirect(request.META.get("HTTP_REFERER"))
        model_class = content_type.model_class()

        # Get the model instance
        model_instance = model_class.objects.filter(id=model_id).first()
        if not model_instance:
            messages.error(request, "Record not found.")
            return redirect(request.META.get("HTTP_REFERER"))

        crop_data = list(map(float, crop_data.split(",")[:4]))
        filename = str(time.time() * 10000)
        new_image = crop_image(getattr(model_instance, field_name),
                               quality=50,
                               crop_data=crop_data,
                               filename=filename)
        # Save photo
        getattr(model_instance, field_name,
                new_image).save(filename, new_image)
        model_instance.save()
        return redirect(request.META.get("HTTP_REFERER"))


class StreamTaskStatusView(View):

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        self.link = "null"

        def get_task_progress():
            retry_count = 0
            while True:
                time.sleep(0.05)
                data = ""
                try:
                    if result.info:
                        self.link = result.info.get("link") or self.link
                        data = str(result.info.get("current", "")) + "/" + str(
                            result.info.get("total",
                                            "")) + " " + result.info.get(
                                                "info", "")
                    if result.status == "SUCCESS":
                        yield 'data: DONE %s\n\n' % self.link
                        break
                    yield 'data: %s\n\n' % data
                except AttributeError as e:
                    yield 'data: Error occured: %s\n\n' % str(e)
                    if retry_count > 20:
                        break
                    retry_count += 1
        return StreamingHttpResponse(get_task_progress(),
                                     content_type='text/event-stream')
