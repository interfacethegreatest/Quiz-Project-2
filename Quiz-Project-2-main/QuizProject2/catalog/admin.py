from django.contrib import admin
from .models import Language, UserProfile, Field, QuestionOption, Question, Test, TestInstance
# Register your models here.

admin.site.register(Language)
admin.site.register(UserProfile)
admin.site.register(Field)
admin.site.register(QuestionOption)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestInstance)