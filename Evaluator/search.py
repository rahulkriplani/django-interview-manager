from Evaluator import models
from django.contrib.auth.models import User
from django.db.models import Q

def global_search(query):
    candidates = models.Candidate.objects.filter(Q(name__contains=query))
    questions = models.Question.objects.filter(Q(description__contains=query))
    vendors = models.Vendor.objects.filter(Q(name__contains=query))
    positions = models.Position.objects.filter(Q(name__contains=query))
    users = User.objects.filter(Q(first_name__contains=query)|Q(last_name__contains=query))
    dict_results = dict()
    if candidates:
        dict_results['candidates'] = candidates

    if questions:
        dict_results['questions'] = questions
    
    if vendors:
        dict_results['vendors'] = vendors
    
    if positions:
        dict_results['positions'] = positions

    if users:
        dict_results['users'] = users

        
    return dict_results

