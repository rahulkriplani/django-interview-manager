# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Candidate
from .models import Position
from .models import Interview
from .models import Question
from .models import Skill, Answer
from .models import QuestionSet

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'difficulty', 'skill', 'qset')
    fieldsets = [
        (None,               {'fields': ['description', 'difficulty', 'skill', 'qset']}),

    ]
    inlines = [AnswerInline]

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(Interview)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Skill)
admin.site.register(QuestionSet)


