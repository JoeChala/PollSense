from django.db import models
from django.conf import settings
import uuid


class Survey(models.Model):
    # contains the available statuses for the survey
    class SurveyStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CLOSED = "CLOSED", "Closed"
        ARCHIVED = "ARCHIVED", "Archived"
    
    survey_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # default user model
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        blank=False,
        max_length=255
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        blank=False,
        choices=SurveyStatus.choices,
        default=SurveyStatus.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    # more types have to be added
    class QuestionTypes(models.TextChoices):
        MCQ = "MCQ", "Multiple Choice"
        TEXT = "TEXT", "Text"
        RATING = "RATING", "Rating"

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")

    question_text = models.TextField(blank=False)

    question_type = models.CharField(
        max_length=20,
        blank=False,
        choices=QuestionTypes.choices,
        default=QuestionTypes.TEXT
    )
    # stores the order of the current question in the survey
    order = models.IntegerField(default=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices",on_delete=models.CASCADE)
    text = models.CharField(max_length=255,blank=False)

class Response(models.Model):
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE,related_name="responses")
    submitted_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    text_answer = models.TextField(null=True, blank=True)
    selected_choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    rating_value = models.IntegerField(null=True, blank=True)

