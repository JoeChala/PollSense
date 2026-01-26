from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import secrets
import string


class SurveyIDField(models.CharField):
    def generate_survey_id(self):
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(10))
    
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_survey_id()
            setattr(model_instance, self.attname, value)
        return value
    

class SurveyIdentity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SurveyRules(models.Model):
    max_responses = models.IntegerField(
        blank=True,
        validators=[MinValueValidator(0)],
        default=0
    )
    
    ip_response_limit = models.IntegerField(
        blank=True,
        validators=[MinValueValidator(0)],
        default=0)

    require_captcha = models.BooleanField(default=False,blank=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(max_responses__gte=0) & models.Q(ip_response_limit__gte=0),
                name="response_limits_non_negative"
            )
        ]
    

class SurveyStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    CLOSED = "closed", "Closed"
    ARCHIVED = "archived", "Archived"

class SurveyLifecycle(models.Model):
    survey_status = models.CharField(
        blank=False,
        null=False,
        choices=SurveyStatus.choices,
        default=SurveyStatus.DRAFT
    )    

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True,blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True,blank=True)

    def save(self,*args,**kwargs) -> None:
        #prevent any changers after gettinf archived
        if self.pk:
            old = type(self).objects.get(pk=self.pk)
            if old.survey_status == SurveyStatus.ARCHIVED:
                raise ValidationError("Archived surveys cannot be modified.")
        
        if self.archived_at is not None:
            self.survey_status = SurveyStatus.ARCHIVED
        
        elif self.closed_at is not None:
            self.survey_status = SurveyStatus.CLOSED
        
        
        elif self.published_at is not None:
            self.survey_status = SurveyStatus.PUBLISHED
        super().save(*args, **kwargs)

    def clean(self):
        new_status = SurveyStatus(self.survey_status)
        #preventing invalid status changes
        if self.pk:
            old = type(self).objects.get(pk=self.pk)
            old_status = SurveyStatus(old.survey_status)

            allowed_transitions = {
                SurveyStatus.DRAFT: {SurveyStatus.PUBLISHED},
                SurveyStatus.PUBLISHED: {SurveyStatus.CLOSED},
                SurveyStatus.CLOSED: {SurveyStatus.ARCHIVED},
                SurveyStatus.ARCHIVED: set(),
            }

            if new_status != old_status:
                if new_status not in allowed_transitions[old_status]:
                    raise ValidationError(
                        f"Invalid transition from {old_status.label} to {new_status.label}"
                    )

        errors = {}

        if new_status == SurveyStatus.PUBLISHED and self.published_at is None:
            errors["published_at"] = "published_at must be set when status is PUBLISHED."

        if new_status == SurveyStatus.CLOSED and self.closed_at is None:
            errors["closed_at"] = "closed_at must be set when status is CLOSED."

        if new_status == SurveyStatus.ARCHIVED and self.archived_at is None:
            errors["archived_at"] = "archived_at must be set when status is ARCHIVED."

        if errors:
            raise ValidationError(errors)


    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(survey_status=SurveyStatus.CLOSED, closed_at__isnull=True),
                name="closed_requires_closed_at",
            ),
            models.CheckConstraint(
            condition=~models.Q(survey_status=SurveyStatus.PUBLISHED, published_at__isnull=True),
            name="published_requires_published_at",
            ),

            models.CheckConstraint(
                condition=~models.Q(survey_status=SurveyStatus.ARCHIVED, archived_at__isnull=True),
                name="archived_requires_archived_at",
            ),
        ]

#main model
class Survey(models.Model):
    survey_id = SurveyIDField(
        max_length=10,
        unique=True,
        editable=False,
    )

    identity = models.OneToOneField(
        to=SurveyIdentity,
        on_delete=models.CASCADE,
        related_name="survey"
    )
    
    rules = models.OneToOneField(
        to=SurveyRules,
        on_delete=models.CASCADE,
        related_name="survey"
    )

    def save(self, *args, **kwargs):
        if not self.identity.slug:
            base = self.identity.title.lower().replace(" ", "-")
            self.slug = f"{base}--{self.survey_id}"
        if self._state.adding:  
            for _ in range(5): 
                try:
                    super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    self.survey_id = None  
            raise IntegrityError("Could not generate a unique survey_id")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.identity.title
