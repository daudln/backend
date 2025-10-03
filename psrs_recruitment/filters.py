from django_filters import rest_framework as filters
from .models import Job


class JobFilter(filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            "title": ["icontains"],
            "company": ["exact"],
            "location": ["exact"],
            "salary": ["gt", "lt"],
        }
