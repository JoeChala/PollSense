from django.urls import path
from . import views

urlpatterns = [
    path(route='list/',view=views.survey_list),
    path(route='<uuid:survey_id>/',view=views.take_survey)
]