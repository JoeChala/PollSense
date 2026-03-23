from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Survey,Question

def home_page(request):
    return render(request,"surveys/home.html")

def user_signin(request):
    return render(request,"surveys/signin.html")

def survey_list(request):
    surveys = Survey.objects.filter(owner=request.user)
    context = {
        'surveys': surveys
    }
    return render(request, 'surveys/survey_list.html', context)

def take_survey(request,survey_id):
    survey = get_object_or_404(Survey,survey_id=survey_id)
    
    if survey.status != Survey.SurveyStatus.PUBLISHED:
        raise Http404(f"This survey is not published\nCurrent status: {survey.status}")
    
    questions = Question.objects.filter(survey=survey).prefetch_related('mcq_choices').order_by('order')
    print(questions)
    context = {
        'questions':questions,
    }

    return render(request, 'surveys/take_survey.html',context)