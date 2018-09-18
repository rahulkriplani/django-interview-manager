# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Candidate
from .models import Position
from .models import Interview
from .models import Question
from .models import Skill, Answer
from .models import QuestionSet

class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('__str__', 'id_code','exp_needed', 'location', 'j_type')

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['description']
    list_filter = ['difficulty', 'skill']
    list_display = ('description', 'difficulty', 'skill')
    fieldsets = [
        (None,               {'fields': ['description', 'difficulty', 'skill', 'qset']}),

    ]
    inlines = [AnswerInline]

class InterviewAdmin(SimpleHistoryAdmin):
    list_display = ('__str__', 'candidate','date', 'position', 'status', 'result')
    search_fields = ['candidate__name']
    list_editable = ['status', 'result']
    list_filter = ['status', 'result']
    history_list_display = ["status", "result"]

admin.site.register(Candidate)
admin.site.register(Position, PositionAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Skill)
admin.site.register(QuestionSet)


