from django.contrib.auth.decorators import login_required
from django.urls import path

from taskupdates.update.views import RecordsView, TaskUpdateView

app_name = "updates"
urlpatterns = [
    path("", login_required(TaskUpdateView.as_view()), name="home"),
    path("records", login_required(RecordsView.as_view()), name="records"),
]
