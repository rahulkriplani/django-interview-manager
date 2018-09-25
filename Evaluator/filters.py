from .models import Interview, Candidate
import django_filters

class InterviewFilter(django_filters.FilterSet):

    class Meta:
        model = Interview
        fields = ['position', 'date', 'result', 'status']


class CandidateFilter(django_filters.FilterSet):

    class Meta:
        model = Candidate
        fields = ['vendor', 'position_applied']
