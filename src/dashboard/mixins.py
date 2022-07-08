from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View

from lms.utils.functions import make_model_key_value


class CreateUpdateMixin(View):
    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        object_id = request.GET.get(self.object_id_field)
        obj = get_object_or_404(self.model_class, id=object_id)
        context = {
            self.object_name: obj,
        }
        if hasattr(self, "get_context_data"):
            context.update(self.get_context_data())
        context.update(make_model_key_value(obj))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        object_id = request.POST.get(self.object_id_field) or -1
        obj = self.model_class.objects.filter(id=object_id).first()
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
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
