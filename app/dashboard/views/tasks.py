from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.html import strip_tags
from accounts.models import User
from dashboard.forms import TaskForm
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Notification, Task
from dashboard.tasks import send_notification
from setup.models import School, SchoolSession
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone


class TasksView(PermissionRequiredMixin, View):
    template_name = "dashboard/tasks/tasks.html"
    permission_required = [
        "dashboard.view_task",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        sessions = SchoolSession.objects.filter(
            deleted=False).order_by("end_date")

        query = request.GET.get("query")
        session_id = request.GET.get("session_id")
        task_status = request.GET.get("task_status")
        if query:
            tasks = tasks.filter(Q(assigned_to__surname__icontains=query) |
                                 Q(message__icontains=query) |
                                 Q(assigned_to__other_names__icontains=query))
        if session_id:
            tasks = tasks.filter(session_id=session_id)
        if task_status:
            tasks = tasks.filter(status=task_status)

        if not request.user.has_perm("setup.manage_tasks"):
            tasks = tasks.filter(assigned_to=request.user)

        context = {
            "tasks": tasks,
            "sessions": sessions,
            **{k: v
               for k, v in request.GET.items()}
        }
        return render(request, self.template_name, context)


class CreateUpdateTaskView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/tasks/edit_task.html"
    form_class = TaskForm
    object_id_field = "task_id"
    model_class = Task
    object_name = "task"
    redirect_url = "dashboard:tasks"
    permission_required = (
        "dashboard.add_task",
        "dashboard.change_task",
    )

    def get_context_data(self):
        sessions = SchoolSession.objects.filter(
            deleted=False).order_by("end_date")
        return {
            "sessions": sessions,
        }

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        object_id = request.POST.get(self.object_id_field) or -1
        username = request.POST.get("username")

        assignee = User.objects.filter(username=username).first()

        obj = self.model_class.objects.filter(id=object_id).first()
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            task = form.save()
            task.assigned_to = assignee
            task.save()
            return redirect(self.redirect_url or "dashboard:index")
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                break
            context = {k: v for k, v in request.POST.items()}
            if hasattr(self, "get_context_data"):
                context.update(self.get_context_data())
            messages.warning(request, message)
            return render(request, self.template_name, context)


class SendTaskNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/tasks/tasks.html"
    permission_required = [
        "dashboard.view_task",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return redirect("dashboard:tasks")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        task_id = request.POST.get("task_id")

        task = get_object_or_404(Task, id=task_id)
        sender_id = School.objects.first().sms_sender_id
        message = task.message
        phone = task.assigned_to.phone
        notification = Notification.objects.create(text=message,
                                                   status="new",
                                                   purpose="TASK_ALERT",
                                                   sender_id=sender_id,
                                                   destination=phone,
                                                   initiated_by=request.user)
        send_notification.delay(notification.id)
        messages.info(request, "Messages queued for delivery successfully.")
        task.notified_at = timezone.now()
        task.save()
        return redirect("dashboard:tasks")
