from django import forms
from django.forms.widgets import Textarea

from taskupdates.update.models import TaskUpdate


class TaskUpdatesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}), required=True
    )
    original_estimate = forms.TimeField(widget=forms.TextInput(attrs={"type": "time"}))

    class Meta:
        model = TaskUpdate
        exclude = (
            "data",
            "assignee",
        )
        widgets = {
            "task": Textarea(attrs={"cols": 2, "rows": 3}),
            "update": Textarea(attrs={"cols": 2, "rows": 3}),
        }

    def save(self, commit=True):
        form = super().save(commit=False)
        form.assignee = self.user
        if commit:
            form.save()
            self.save_m2m()
        return form
