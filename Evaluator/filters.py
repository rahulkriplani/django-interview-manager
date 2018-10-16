from .models import Interview, Candidate
import django_filters
from django.contrib.admin.widgets import AdminDateWidget

class InterviewFilter(django_filters.FilterSet):

	start_date = django_filters.DateFilter(name='date',lookup_expr=('gt'), widget=AdminDateWidget())
	end_date = django_filters.DateFilter(name='date',lookup_expr=('lt'), widget=AdminDateWidget()) 
	registry_year = django_filters.DateRangeFilter(field_name='date', lookup_expr='year')

	class Meta:
		model = Interview
		fields = ['position', 'result', 'status']


class CandidateFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(name='created_at',lookup_expr=('gt'), widget=AdminDateWidget())
    end_date = django_filters.DateFilter(name='created_at',lookup_expr=('lt'), widget=AdminDateWidget())
    registry_year = django_filters.DateRangeFilter(field_name='created_at', lookup_expr='year')

    class Meta:
        model = Candidate
        fields = ['vendor', 'position_applied']
