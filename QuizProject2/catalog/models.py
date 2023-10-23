from django.db import models
from django.urls import reverse

# Create your models here.

class Language(models.Model):
    "Model representing a language for question"
    language = models.CharField(max_length=200, help_text='Enter a Language (e.g. English)')
    def __str__(self):
        """String for representing the Model object."""
        return self.language

class Author(models.Model):
    "Model Representing an author for a quiz or question."
    first_name = models.CharField(max_length =30, help_text='Enter your first name.')
    last_name = models.CharField(max_length =30, help_text='Enter your last name.')
    def __str__(self):
        """String for representing the Model Object."""
        return self.first_name + " " + self.last_name


class Field(models.Model):
    """Model representing a test field."""
    name = models.CharField(max_length = 200, help_text = 'Enter a test field (e.g. Science')

    def __str__(self):
        """String for representing the Model Object."""
        return self.name

class Options(models.Model):
    """Model represeting the options a user can select between for a question."""
    id = models.UUIDField(primary_key = True, default = uuid4, help_text='Unique ID for this particular option.')
    option = models.CharField(max_length = 1000, help_text = 'Enter an option, this specifies an option the user will either have to enter or select from.')

class Question(models.Model):
     """Model representing a specific copy of a question (i.e. that can be part of a test). Choose multiple choice or fill in the gaps."""
     id = models.UUIDField(primary_key = True, default = uuid4, help_text='Unique ID for this particular question across whole website.')
     genre = models.ManyToManyField(Genre, help_text = 'designate a queryable genre for the question e.g maths or Welding for example.')
     
    QUESTION_CHOICES = (
        ('m', 'Multiple Choices'),
        ('f', 'Fill in the Gaps'),
        ('i', 'Multiple choice + image')
    )

     question_type = models.CharField(
        max_length =1,
        choices = QUESTION_CHOICES,
        blank = True,
        default = 'm',
        help_text='question type'
     )
     title = models.TextField(max_length = 1000, help_text='Enter a brief title for the question, e.g. On Convection.... :')
     text = models.TextField(max_length = 3000, help_text = 'Here you should supply the question text, e.g. what is 2+2? or a two paragraphs of text which the user can select between multiple choices of their validity.')
     option = models.ManyToManyField(Options, on_delete = models.SET_NULL, null=True)
     image = models.ImageField(help_text = ' optional image for image type or just adittional help.')
     answer = models.ManyToManyField(Options, on_delete = models.Set_NULL, null = True, 'Choose a sub-selection of options. These will be matched to the options to determine a correct answer.')
     correct = models.BooleanField(default=False, 'set to True if answer is marked to be correct.')
     def __str(self):
        """String for representing the question,"""
        return self.id + ": " self.text




class Test(models.Model):
    """Model representing a exam(but not a specific exam)."""
    title = models.CharField(max_length = 200, help_text = 'Enter a name for your test. A module name or a general title.')
    author = models.ForeignKey(Author, on_delete = models.SET_NULL, null = True)
    summary = models.TextField(max_length = 1000, help_text='Enter a brief description of the Test')
    genre = models.ManyToManyField(Genre, help_text ='Select a genre for this test.')
    question = models.ManyToManyField(Question, on_delete=models.SET_NULL, null=True)
    


    def __str__(self):
        return self.title

class TestInstance(models.Model):
    "Model representing an instance of an exam."
    id = models.UUIDField(primary_key = True, default = uuid4, help_text='Indentifier of an Exam instance, unique ID.')]
    duration = models.DurationField()
    start_time = models.DateTimeField(default=timezone.now)
    countdown_expired = models.BooleanField(default=False)
    EXAM_STATUS = (
        ('u', 'Undergoing'),
        ('c', 'Completed'),
        ('n', 'Not started.'),
    )

    status = models.CharField(
        max_length =1,
        choices = LOAN_STATUS,
        blank = False,
        default ='u',
        help_text = 'Current exam status.'
    )

    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)



    def time_remaining(self):
        elapsed_time = timezone.now() - self.start_time
        remaining_time = self.duration - elapsed_time
        return max(remaining_time, timezone.timedelta())

    def is_expired(self):
        return self.time_remaining() == timezone.timedelta()
    
    def __str__(self):
        return self.id + " " + self.exam + " : " + str(time_remaining())
