from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid


class Survey(models.Model):
    # contains the available statuses for the survey
    class SurveyStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CLOSED = "CLOSED", "Closed"
        ARCHIVED = "ARCHIVED", "Archived"
    # contains current visibility options
    class SurveyVisibility(models.TextChoices):
        PUBLIC = "PUBLIC", "Public"
        PRIVATE = "PRIVATE", "Private"

    survey_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False, 
        unique=True)

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

    visibility = models.CharField(
        max_length=20,
        choices=SurveyVisibility.choices,
        default=SurveyVisibility.PRIVATE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


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
    order = models.PositiveIntegerField(default=1)

    is_required = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('survey', 'order')


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices",on_delete=models.CASCADE)
    
    text = models.CharField(max_length=255,blank=False)

    order = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('question','order')


class Response(models.Model):
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE,related_name="responses",db_index=True)

    submitted_at = models.DateTimeField(auto_now_add=True,db_index=True)

    metadata = models.JSONField(null=True, blank=True)


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,db_index=True)

    text_answer = models.TextField(null=True, blank=True)
    selected_choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    rating_value = models.IntegerField(null=True, blank=True)

    def clean(self):
        if self.question.question_type == Question.QuestionTypes.MCQ and not self.selected_choice:
            raise ValidationError("MCQ requires selected_choice")

        if self.question.question_type == Question.QuestionTypes.TEXT and not self.text_answer:
            raise ValidationError("Text question requires text_answer")

