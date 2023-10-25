from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
import uuid

class Language(models.Model):
    class LanguageChoices(models.TextChoices):
        ENGLISH = 'English', _('English')
        SPANISH = 'Spanish', _('Spanish')
        FRENCH = 'French', _('French')
        # Add more language choices as needed

    language = models.CharField(
        max_length=100,
        choices=LanguageChoices.choices,
        unique=True,
        help_text=_('Select a language for the question (e.g. English)')
    )

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return self.get_language_display()


from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, help_text='Enter your first name')
    last_name = models.CharField(max_length=30, help_text='Enter your last name')

    def __str__(self):
        return f'{self.user.username} Profile'


class Field(models.Model):
    name = models.CharField(
        max_length=200,
        help_text=_('Enter a test field (e.g. Science)')
    )

    class Meta:
        verbose_name = _('Test Field')
        verbose_name_plural = _('Test Fields')

    def __str__(self):
        return self.name

class QuestionOption(models.Model):
    """Model representing the options a user can select for a question."""
    option = models.CharField(max_length=200, help_text='Enter an option for the question.')

    def __str__(self):
        return self.option


class Question(models.Model):
    """Model representing a specific copy of a question that can be part of a test."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular question across the whole website.')
    field = models.ManyToManyField(Field, help_text='Designate a queryable genre for the question (e.g. maths or Welding).')
    QUESTION_CHOICES = (
        ('m', _('Multiple Choices')),
        ('f', _('Fill in the Gaps')),
        ('i', _('Multiple choice + image')),
    )

    question_type = models.CharField(
        max_length=1,
        choices=QUESTION_CHOICES,
        default='m',
        help_text=_('Question type')
    )
    title = models.TextField(max_length=1000, help_text='Enter a brief title for the question (e.g., On Convection...).')
    text = models.TextField(max_length=3000, help_text='Supply the question text (e.g., What is 2+2?) or a longer text for multiple choice options.')

    options = models.ManyToManyField(QuestionOption, help_text='Options for this question.')
    image = models.ImageField(blank=True, help_text='Optional image for image type or additional help.')
    answer = models.ForeignKey(QuestionOption, on_delete=models.SET_NULL, null=True, help_text='Choose the correct answer option.', related_name='correct_for')
    correct = models.BooleanField(default=False, help_text='Leave empty if in creation.')

    def __str__(self):
        return self.text


class Test(models.Model):
    """Model representing an exam (but not a specific exam)."""
    title = models.CharField(max_length=200, help_text='Enter a name for your test, e.g., module name or general title.')
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=100, help_text='Enter a brief description of the Test.')
    genre = models.ManyToManyField(Field, help_text='Select a genre for this test.')
    questions = models.ManyToManyField(Question, help_text='Select questions for this test.')

    # Additional fields
    duration = models.DurationField(help_text='Time limit to complete the test')
    passing_score = models.PositiveIntegerField(help_text='Passing score required to pass the test')
    difficulty_level = models.CharField(
        max_length=100,
        help_text='Difficulty level of the test (e.g., easy, medium, difficult)'
    )
    published_date = models.DateField(help_text='Date when the test was published')
    is_public = models.BooleanField(default=True, help_text='Set to True if the test is public')
    total_score = models.PositiveIntegerField(help_text='Total marks or score for the test. Set to zero if not attempted.')

    def __str__(self):
        return self.title

from django.utils import timezone

class TestInstance(models.Model):
    "Model representing an instance of an exam."
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Identifier of an Exam instance, unique ID.')
    start_time = models.DateTimeField(default=timezone.now)
    countdown_expired = models.BooleanField(default=False)
    EXAM_STATUS = (
        ('u', 'Undergoing'),
        ('c', 'Completed'),
        ('n', 'Not started'),
    )

    status = models.CharField(
        max_length=1,
        choices=EXAM_STATUS,
        default='n',
        help_text='Current exam status.'
    )

    exam = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)

    # Additional fields
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='User taking the test')
    score = models.PositiveIntegerField(default=0, help_text='Score achieved in the test instance')
    submission_time = models.DateTimeField(null=True, blank=True, help_text='Time when the user submitted the test')

    def get_duration(self):
        return self.exam.duration

    def time_remaining(self):
        elapsed_time = timezone.now() - self.start_time
        remaining_time = self.get_duration() - elapsed_time
        return max(remaining_time, timezone.timedelta())

    def is_expired(self):
     if self.time_remaining() == timezone.timedelta():
        self.status = 'c'  # Change status to 'Completed'
        self.countdown_expired = True
        self.save()  # Save the changes
        return True
     return False

    def __str__(self):
        return f"{self.id} {self.exam} : {self.start_time}"
