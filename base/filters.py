import django_filters
from .models import *

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {'state':['exact'],'function':['exact'],'name':['exact'],'dept':['exact'],'customer':['exact'],'year':['exact'],'date':['exact'],'operation':['exact'],'fraction':['exact']}

class defaultProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {'state':['exact'],'function':['exact'],'name':['exact'],'customer':['exact'],'year':['exact'],'operation':['exact'],'fraction':['exact']}

class responsibleFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = {'name':['exact'],}