from django.urls import path
from . import views

urlpatterns = [
    path(route='',view=views.survey_list),
    path(route='s/<uuid:survey_id>/',view=views.take_survey)
]