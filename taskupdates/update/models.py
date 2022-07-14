from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from taskupdates.utils.models import BaseModel


class TaskUpdate(BaseModel):
    assignee = models.ForeignKey(
        "users.User", related_name="updates", on_delete=models.CASCADE
    )
    task = models.TextField()
    date = models.DateField()
    original_estimate = models.TimeField()
    update = models.TextField()
    data = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.assignee.username}"

    class Meta:
        db_table = "update"
        verbose_name = _("Update")
        verbose_name_plural = _("Updates")

    def get_absolute_url(self):
        return reverse("update:records")
