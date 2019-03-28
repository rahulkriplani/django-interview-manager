from modules import *

#***********************************************************************
#-------------------------------- Openings ---------------------------
#***********************************************************************

def all_openings(request):
    openings = JobOpening.objects.all()
    return render(request, 'Evaluator/job_openings.html', {'openings': openings})
