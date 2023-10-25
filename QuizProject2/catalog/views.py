from django.shortcuts import render
# Create your views here.
from .models import Language, UserProfile, Field, QuestionOption, Question, Test, TestInstance

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_quizzes = Test.objects.all().count()
    num_instances = TestInstance.objects.all().count()
    num_questions = TestInstance.objects.all().count()

    # The 'all()' is implied by default.
    num_authors = UserProfile.objects.count()

    context = {
        'num_books': num_quizzes,
        'num_instances': num_instances,
        'num_questions': num_questions,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
