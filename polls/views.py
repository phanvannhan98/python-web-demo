from django.shortcuts import render, redirect
from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    """The home page for Polls app."""
    return render(request, 'polls/index.html')
# Login required
@login_required
def questions(request):
    """Show all questions"""
    # Query the database for all questions
    # questions = Question.objects.all()
    # Retrieve the questions whose owner matches the current user
    questions = Question.objects.filter(owner=request.user)
    # Context that will send to the template
    context = {'questions': questions}
    return render(request, 'polls/questions.html', context)

@login_required
def question(request, question_id):
    """Show a single question and all its choices"""
    # Select the question which id is question_id
    question = Question.objects.get(id=question_id)

    # Ensure the questin belongs to the current user
    if question.owner != request.user:
        raise Http404


    # Query all choice related to this question
    choices = question.choice_set.all()
    # Context
    context = {'question': question, 'choices': choices}
    return render(request, 'polls/question.html', context)

@login_required
def new_question(request):
    """Add a new question"""
    # Initially request method is GET
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = QuestionForm()
    else:
        # POST data submitted; process data.
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            # form.save()
            # Associtating new question with the current user
            new_question = form.save(commit=False)
            new_question.owner = request.user
            new_question.save()
            return redirect('polls:questions')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'polls/new_question.html', context)

@login_required
def new_choice(request, question_id):
    """Add a new choice for particular question"""
    # Select the specific question to add new choice
    question = Question.objects.get(id=question_id)

    if request.method != 'POST':
        # No data submitted; create a blank form
        form = ChoiceForm()
    else:
        # POST data submitted; process data.
        form = ChoiceForm(data=request.POST)
        if form.is_valid():
            # Create new choice object without saving it to the database
            new_choice = form.save(commit=False)
            # Set the question attribute of new_choice
            new_choice.question = question
            new_choice.save()
            return redirect('polls:question', question_id=question_id)

    # Display a blank or invalid form
    context = {'question': question, 'form': form}
    return render(request, 'polls/new_choice.html', context)
