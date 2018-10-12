from Evaluator import models
from django.db.models import Q

def global_search(query):
    candidates = models.Candidate.objects.filter(Q(name__contains=query))
    questions = models.Question.objects.filter(Q(description__contains=query))
    vendors = models.Vendor.objects.filter(Q(name__contains=query))
    positions = models.Position.objects.filter(Q(name__contains=query))
    dict_results = dict()
    if candidates:
        dict_results['candidates'] = candidates

    if questions:
        dict_results['questions'] = questions
    
    if vendors:
        dict_results['vendors'] = vendors
    
    if positions:
        dict_results['positions'] = positions
        
    return dict_results

