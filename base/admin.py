from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import CSorSMARTMNF, Completion, Department, Fractions, Function, Project, State, customer, \
    operationType, plannedYear, proggresStage, digitalMaturity, maturityCof, connectivity, connectivityCof, \
    Item, Weight, complexity, impTime, impCoff, yes_no

admin.site.register(Project)
admin.site.register(State)
admin.site.register(Function)
admin.site.register(Department)
admin.site.register(CSorSMARTMNF)
admin.site.register(complexity)
admin.site.register(operationType)
admin.site.register(customer)
admin.site.register(proggresStage)
admin.site.register(Fractions)
admin.site.register(Completion)
admin.site.register(plannedYear)
admin.site.register(impTime)
admin.site.register(impCoff)
admin.site.register(digitalMaturity)
admin.site.register(maturityCof)
admin.site.register(connectivity)
admin.site.register(connectivityCof)
admin.site.register(Item)
admin.site.register(yes_no)
admin.site.register(Weight)
