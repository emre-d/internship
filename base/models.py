import decimal

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Function(models.Model):
    name = models.CharField(max_length=200,verbose_name="Add function")

    def __str__(self):
        return str(self.name)

class smartMNF(models.Model):
    mnfcoff = models.IntegerField()

    def __str__(self):
        return str(self.mnfcoff)

class CSorSMARTMNF(models.Model):
    name = models.CharField(max_length=200)
    mnf = models.ForeignKey(smartMNF,on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str(self.name)


class Department(models.Model):
    name = models.CharField(max_length=200,verbose_name="Enter department name")
    resp = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)

class operationType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class customer(models.Model):
    name = models.CharField(max_length=200,verbose_name="Add Customer type")

    def __str__(self):
        return self.name


class plannedYear(models.Model):
    name = models.CharField(max_length=200,verbose_name="Add Planned Year as MMMM-YY")

    def __str__(self):
        return self.name


class proggresStage(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Completion(models.Model):
    name = models.CharField(max_length=200,verbose_name="Add Completion Date")

    def __str__(self):
        return self.name


class Fractions(models.Model):
    name = models.DecimalField( max_digits = 5,
                         decimal_places = 1,verbose_name="Add Fraction")

    def __str__(self):
        return str(self.name)


class Weight(models.Model):
    weight = models.DecimalField(max_digits=100,decimal_places=1)

    def __str__(self):
        return str(self.weight)

class Item(models.Model):
    item = models.CharField(max_length=200,blank=True,null=True)
    wgt = models.ForeignKey(Weight, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return str(self.item)
class maturityCof(models.Model):
    coff = models.IntegerField()

    def __str__(self):
        return str(self.coff)

class digitalMaturity(models.Model):
    maturity = models.CharField(max_length=200,blank=True,null=True)
    coff = models.ForeignKey(maturityCof, on_delete=models.SET_NULL, null=True,blank=True)
    def __str__(self):
        return str(self.maturity)

class connectivityCof(models.Model):
    conn = models.IntegerField()

    def __str__(self):
        return str(self.conn)

class connectivity(models.Model):
    connectivity = models.CharField(max_length=200, blank=True, null=True)
    conn = models.ForeignKey(connectivityCof, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.connectivity)

class impCoff(models.Model):
    imp = models.IntegerField()

    def __str__(self):
        return str(self.imp)

class impTime(models.Model):
    implemTime = models.CharField(max_length=200, blank=True, null=True)
    impcoff = models.ForeignKey(impCoff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.implemTime)
class complexity(models.Model):
    complexity = models.IntegerField()

    def __str__(self):
        return str(self.complexity)

class oldStatus(models.Model):
    old_status = models.CharField(max_length=200,blank=True,null=True)
    project_id = models.CharField(max_length=200,blank=True,null=True)
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.old_status)

class yes_no(models.Model):
    option = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return str(self.option)

class Project(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    function = models.ForeignKey(Function, on_delete=models.SET_NULL, null=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200,null=True,verbose_name="Project Name")
    index = models.DecimalField(max_digits = 5,
                         decimal_places = 2,blank=True,null=True)
    conn = models.ForeignKey(connectivity,on_delete=models.SET_NULL, null=True)
    digital = models.ForeignKey(digitalMaturity,on_delete=models.SET_NULL, null=True)
    short = models.CharField(max_length=100,null=True,blank=True)
    impVar = models.ForeignKey(impTime,on_delete=models.SET_NULL, null=True,verbose_name="Implementation Time")
    complexity = models.ForeignKey(complexity,on_delete=models.SET_NULL, null=True)
    CS_or_SmartMNF = models.ForeignKey(CSorSMARTMNF, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(yes_no, on_delete=models.SET_NULL, null=True,verbose_name="Manufacturing Automation")
    date = models.ForeignKey(Completion, on_delete=models.SET_NULL, null=True,blank=True)
    year = models.ForeignKey(plannedYear, on_delete=models.SET_NULL, null=True)
    fraction = models.ForeignKey(Fractions, on_delete=models.SET_NULL, null=True)
    operation = models.ForeignKey(operationType,on_delete=models.SET_NULL,null=True, blank=True)
    latestStatus = models.TextField(max_length=200, null=True)
    details = models.TextField(max_length=200, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id', '-dept']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.option.__str__() == 'Yes':
                self.date = None
                frac = self.fraction.name
                self.index = round((float(frac) * (float(self.digital.coff.__str__())*float(Weight.objects.get(id=1).__str__())) * ((float(self.complexity.__str__())*float(Weight.objects.get(id=2).__str__())) + (float(self.impVar.impcoff.__str__())*float(Weight.objects.get(id=3).__str__())))*((float(2*float(Weight.objects.get(id=4).__str__())))+(float(self.conn.conn.__str__())*float(Weight.objects.get(id=5).__str__())))))
                super().save(*args, **kwargs)
            elif self.option.__str__() == 'No':
                self.date = None
                frac = self.fraction.name
                self.index = round((float(frac) * (float(self.digital.coff.__str__())*float(Weight.objects.get(id=1).__str__())) * ((float(self.complexity.__str__())*float(Weight.objects.get(id=2).__str__())) + (float(self.impVar.impcoff.__str__())*float(Weight.objects.get(id=3).__str__())))*((float(1*float(Weight.objects.get(id=4).__str__())))+(float(self.conn.conn.__str__())*float(Weight.objects.get(id=5).__str__())))))
                super().save(*args, **kwargs)
        elif not self._state.adding:
            if self.option.__str__() == 'Yes':
                frac = self.fraction.name
                self.index = round((float(frac) * (float(self.digital.coff.__str__()) * float(Weight.objects.get(id=1).__str__())) * (
                            (float(self.complexity.__str__()) * float(Weight.objects.get(id=2).__str__())) + (
                                float(self.impVar.impcoff.__str__()) * float(Weight.objects.get(id=3).__str__()))) * ((float(2 * float(Weight.objects.get(id=4).__str__()))) + (
                            float(self.conn.conn.__str__()) * float(Weight.objects.get(id=5).__str__())))))
                oldStatus.objects.create(old_status=self.latestStatus, project_id=self.pk)
                super().save(*args, **kwargs)
            elif self.option.__str__() == 'No':
                frac = self.fraction.name
                self.index = round((float(frac) * (float(self.digital.coff.__str__()) * float(Weight.objects.get(id=1).__str__())) * (
                            (float(self.complexity.__str__()) * float(Weight.objects.get(id=2).__str__())) + (
                                float(self.impVar.impcoff.__str__()) * float(Weight.objects.get(id=3).__str__()))) * ((float(1 * float(Weight.objects.get(id=4).__str__()))) + (
                            float(self.conn.conn.__str__()) * float(Weight.objects.get(id=5).__str__())))))
                oldStatus.objects.create(old_status=self.latestStatus, project_id=self.pk)
                super().save(*args, **kwargs)

    @property
    def coffcalc(self):
      total =   (float(self.digital.coff.__str__()) * 4)
      return total


