from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.html import strip_tags
from dashboard.forms import InventoryForm, IssuanceForm
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Inventory, Issuance, User
from django.contrib import messages
from django.db.models import Q
from django.utils.html import strip_tags
from lms.utils.functions import make_model_key_value
from django.http import Http404


class InventoryIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/inventory/index.html"
    permission_required = [
        "setup.view_inventory",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        inventories = Inventory.objects.filter(deleted=False)
        query = request.GET.get("query")
        if query:
            inventories = inventories.filter(
                Q(id__contains=query) | Q(name__icontains=query))

        context = {
            "inventories": inventories[:300],
            **{k: v
               for k, v in request.GET.items()},
        }
        return render(request, self.template_name, context)


class InventoriesView(PermissionRequiredMixin, View):
    template_name = "dashboard/inventory/inventory.html"
    permission_required = [
        "setup.view_inventory",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        inventories = Inventory.objects.filter(deleted=False)
        query = request.GET.get("query")
        if query:
            inventories = inventories.filter(
                Q(id__contains=query) | Q(name__icontains=query))

        context = {
            "inventories": inventories[:300],
            **{k: v
               for k, v in request.GET.items()},
        }
        return render(request, self.template_name, context)


class CreateUpdateInventoryView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/inventory/edit_inventory.html"
    form_class = InventoryForm
    object_id_field = "inventory_id"
    model_class = Inventory
    object_name = "inventory"
    redirect_url = "dashboard:inventories"
    permission_required = (
        "setup.add_inventory",
        "setup.change_inventory",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        object_id = request.POST.get(self.object_id_field) or -1
        obj = self.model_class.objects.filter(id=object_id).first()
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user
            inventory.save()
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


class IssuanceView(PermissionRequiredMixin, View):
    template_name = "dashboard/inventory/issuance.html"
    permission_required = [
        "setup.view_issuance",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        issuance = Issuance.objects.filter(deleted=False)
        query = request.GET.get("query")
        if query:
            issuance = issuance.filter(
                Q(id__contains=query) | Q(item__name__icontains=query))

        context = {
            "issuance": issuance[:300],
            **{k: v
               for k, v in request.GET.items()},
        }
        return render(request, self.template_name, context)


class CreateUpdateIssuanceView(PermissionRequiredMixin, View):
    template_name = "dashboard/inventory/edit_issuance.html"
    form_class = IssuanceForm
    object_id_field = "issuance_id"
    model_class = Issuance
    object_name = "issuance"
    redirect_url = "dashboard:issuance"
    permission_required = (
        "setup.add_issuance",
        "setup.change_issuance",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        object_id = request.GET.get(self.object_id_field) or -1
        inventory_id = request.GET.get("inventory_id") or -1
        issuance = Issuance.objects.filter(id=object_id).first()
        inventory = Inventory.objects.filter(id=inventory_id).first() or (
            issuance.item if issuance else None)

        if not (issuance or inventory):
            raise Http404

        current_quatity = issuance.quantity if issuance else 0
        context = {
            "inventory": inventory,
            "issuance": issuance,
            "max_quanity": inventory.remain_quantity + current_quatity,
            "username": issuance.recipient.username if issuance else ""
        }
        if issuance:
            context.update(make_model_key_value(issuance))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        object_id = request.POST.get(self.object_id_field) or -1
        obj = self.model_class.objects.filter(id=object_id).first()
        username = request.POST.get("username")

        recipient = User.objects.filter(username=username).first()
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.recipient = recipient
            inventory.updated_by = request.user
            if not obj:
                inventory.issued_by = request.user
            inventory.save()
            return redirect(self.redirect_url or "dashboard:index")
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                break
            context = {k: v for k, v in request.POST.items()}
            messages.warning(request, message)
            return redirect(
                reverse("dashboard:create_update_issuance") +
                f"?inventory_id={object_id}")
