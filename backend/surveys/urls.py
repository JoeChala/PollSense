from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='auth/signin/',view=views.user_signin),
    path(route='surveys/',view=views.survey_list),
    path(route='s/<uuid:survey_id>/',view=views.take_survey)
]