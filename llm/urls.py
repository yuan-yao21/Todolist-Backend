from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/llm/summarynote", views.llm_request_summarynote, name="llm_request"),
]
