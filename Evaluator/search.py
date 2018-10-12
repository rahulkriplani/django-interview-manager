from Evaluator import models
from django.db.models import Q

def global_search(query):
    candidates = models.Candidate.objects.filter(Q(name__contains=query))
    questions = models.Question.objects.filter(Q(description__contains=query))
    vendors = models.Vendor.objects.filter(Q(name__contains=query))
    positions = models.Position.objects.filter(Q(name__contains=query))
    return {
        'candidates': candidates,
        'questions': questions,
        'vendors': vendors,
        'positions': positions
          }
