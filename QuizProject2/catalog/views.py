from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
# Create your views here.
from .models import *
from .models import Language, UserProfile, Field, QuestionOption, Question, Test, TestInstance
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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

def new_page_view1(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + ' ' + user)
            return redirect('new_page')

    context ={'form':form}
    return render (request, 'createAccount.html', context)

def new_page_view2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #context = {'username': user.username}  # Include the username in the context
            return redirect('user_profile', username=user.username)  # Render the new page
        else:
            messages.info(request, 'Username OR password is incorrect.')

    context = {}
    return render(request, 'login.html', context)


def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {'user' : user}
    return render(request, 'user_profile.html', context)