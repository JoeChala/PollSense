from django.contrib import admin
from .models import Survey, Question, MCQChoice

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(MCQChoice)