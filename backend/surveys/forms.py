from typing import Any, Mapping

from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Question

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions',[])
        
        super().__init__(*args, **kwargs)

        for q in questions:
            field_name = f"question_{q.id}"

            label = q.question_text
            required = q.is_required

            # TEXT
            if q.question_type == Question.QuestionTypes.TEXT:
                self.fields[field_name] = forms.CharField(
                    label=label,
                    required=required
                )

            # MCQ
            elif q.question_type == Question.QuestionTypes.MCQ:
                choices = [(c.id, c.text) for c in q.choices.all()]

                self.fields[field_name] = forms.ChoiceField(
                    label=label,
                    choices=choices,
                    required=required,
                    widget=forms.RadioSelect 
                )

            # RATING
            elif q.question_type == Question.QuestionTypes.RATING:
                choices = [(i, str(i)) for i in range(1, 6)]  # 1–5 rating

                self.fields[field_name] = forms.ChoiceField(
                    label=label,
                    choices=choices,
                    required=required,
                    widget=forms.RadioSelect
                )