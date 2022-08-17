from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import  models
from django import forms
from django.forms import ModelForm
from django.http import request

from .models import Project, Function, operationType, Department, Fractions, State, customer, Completion, \
    plannedYear, CSorSMARTMNF, Weight


#kullanıcı kayıt olma formu
class signUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

#proje ekleme formu host alanını otomatik olarak projeyi oluşturan kişi olarak algılıyor
#departman ise veri tabanında kullanıcıyla ilişkili olduğu için proje oluşturulurken direkt kullanıcının bağlı olduğu departman olarak algılıyor
#örnek olarak alper lastik departmanında. Proje oluşturulurken departman seçmeye gerek kalmadan alperi seçtiğinizde tabloda departmanı gözükür
class ProjectForm(ModelForm):
    class Meta:
            model = Project
            fields = '__all__'
            exclude = ['host','index','short',]

#Aşağıdakilerin hepsi var olan veritabanındaki tablolara veri eklemek için oluşturulan form kodları
class addColumnForm(ModelForm):
    class Meta:
        model = Function
        fields = '__all__'

class addDepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ('name',)

class addResponsibleForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class addFractionForm(ModelForm):
    class Meta:
        model = Fractions
        fields = '__all__'

class addOperationForm(ModelForm):
    class Meta:
        model = operationType
        fields = '__all__'

class updateWeightForm(ModelForm):
    class Meta:
        model = Weight
        fields = '__all__'
class addStateForm(ModelForm):
    class Meta:
        model = State
        fields = '__all__'

class addCustomerForm(ModelForm):
    class Meta:
        model = customer
        fields = '__all__'

class addCompletionForm(ModelForm):
    class Meta:
        model = Completion
        fields = '__all__'

class addYearForm(ModelForm):
    class Meta:
        model = plannedYear
        fields = '__all__'

class updateUserForm(ModelForm):
    class Meta:
        model = Department
        fields = ('resp',)

class addMNFForm(ModelForm):
    class Meta:
        model = CSorSMARTMNF
        fields = '__all__'