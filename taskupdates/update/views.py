from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from taskupdates.update.forms import TaskFilterForm, TaskUpdatesForm
from taskupdates.update.models import TaskUpdate
from taskupdates.users.models import User


class RecordsView(View):
    template_name = "pages/records.html"

    def get(self, request, *args, **kwargs):
        form = TaskFilterForm()
        records = TaskUpdate.objects.order_by("-created_at")
        return render(request, self.template_name, {"records": records, "form": form})

    def post(self, request, *args, **kwargs):
        form = TaskFilterForm(request.POST)
        records = TaskUpdate.objects.order_by("-created_at")
        if form.is_valid():
            assignees = form.cleaned_data.get("assignees")
            date = form.cleaned_data.get("date")
            if assignees and date:
                records = TaskUpdate.objects.filter(assignee_id=assignees.id, date=date)
            elif assignees:
                records = TaskUpdate.objects.filter(assignee_id=assignees.id)
            elif date:
                records = TaskUpdate.objects.filter(date=date)
        context = {"records": records, "form": form}
        return render(request, self.template_name, context)


class TaskUpdateView(View):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        form = TaskUpdatesForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskUpdatesForm(request.POST, user=request.user)

        if form.is_valid():
            form.save(commit=False)
            form.assignee = User.objects.get(id=request.user.id)
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Your Update has been recorded"
            )
            return redirect("update:records")
        context = {"form": form}
        return render(request, self.template_name, context)
