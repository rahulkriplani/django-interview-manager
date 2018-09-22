from .models import Interview
import django_filters

class InterviewFilter(django_filters.FilterSet):
    class Meta:
        model = Interview
        fields = ['position', 'date', 'result', 'status']