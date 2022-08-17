import datetime

from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from . import models
from .filters import ProjectFilter, defaultProjectFilter, responsibleFilter
from .models import Department, Project, State, Function, Fractions, operationType, Weight, oldStatus, complexity, Item
from django.contrib.auth.models import User
from .forms import ProjectForm, addColumnForm, addResponsibleForm, addYearForm, addMNFForm, addStateForm, \
    addCompletionForm, addCustomerForm, addOperationForm, addFractionForm, updateUserForm, addDepartmentForm, \
    signUpForm, updateWeightForm
import xlwt
import pandas as pd
import numpy as np
# Create your views here.

#login sayfası kodları
def loginPage(request):
    page = 'login'
    #burda kullanıcı eğer giriş yapmışsa ana sayfaya yonlendiriyor
    if request.user.is_authenticated:
        return redirect('home')

    #formdan değerleri alma
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username == username)
        except:
            messages.error(request, '')

        #eğer kullanıcı adı şifreyle uyuşuyosa girişe izin verip ana sayfaya yonlendir
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            #eğer uyuşmuyorsa kullanıcı adı veya şifre hatalı mesajı
            messages.error(request, 'Username or pwd is wrong')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    page = 'register'
    form = signUpForm()
    replace = ('@','.','+','-')
    if request.method == 'POST':
        form =signUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            for r in replace:
                user.username = str(user.username).replace(r,'_')
            user.first_name = user.username.split('_')
            user.first_name = str(user.first_name[0]).capitalize() + " " + str(user.first_name[1]).capitalize()
            user.save()
            #login(request, user)
            return redirect('home')
    return render(request, 'base/login_register.html', {'form': form})

#admin sayfası için gerekli kodlar
def superUser(request):
  if request.user.is_superuser:
    item = Item.objects.all()
    weight = Weight.objects.all()
    projects = Project.objects.all()
    project_count = projects.count()
    dept = Department.objects.all()
    user_list = Department.objects.all()
    #kullanıcı filtreleme
    respFilter = responsibleFilter(request.GET,queryset=user_list)
    context = { 'project_count': project_count,
                'w':weight,
                'it':item,
                'user_list': user_list,'respFilter':respFilter,'dept':dept,'projects':projects}
    return render(request, 'base/superuser.html',context)
  else:
      #eğer admin(superuser) dışında biri girmeye çalışırsa ana sayfaya geri yönlendiriliyo
      return redirect('home')

def stat(request):
    if request.user.is_superuser:
        project = Project.objects.all()
        department = Department.objects.all()
        op = operationType.objects.all()
        dept = {
        'PD':Project.objects.filter(dept__name='Product Development').count(),
        'QA':Project.objects.filter(dept__name='QA').count(),
        'MESPT':Project.objects.filter(dept__name='Mixer, Extruder, Stock Prep. Tech.').count(),
        'TBCM':Project.objects.filter(dept__name='Tire Building, Curing, MoldTech').count(),
        'CD':Project.objects.filter(dept__name='Compound Development').count(),
        'MD':Project.objects.filter(dept__name='Material Development').count(),
        'NPD':Project.objects.filter(dept__name='Process Development').count(),
        'MDR':Project.objects.filter(dept__name='Mold Development & Regulation').count(),
        'STPP':Project.objects.filter(dept__name='Stock Prep. Production').count(),
        'ED':Project.objects.filter(dept__name='Eng. Directorate').count(),
        'PC':Project.objects.filter(dept__name='Product Control').count(),
        'IE':Project.objects.filter(dept__name='IE').count(),
        'UT':Project.objects.filter(dept__name='Utility').count(),
        'SMART':Project.objects.filter(dept__name='Smart Prd. & Mnf. Sln. Dev.').count(),
        'HSE':Project.objects.filter(dept__name='HSE').count(),
        'TBP':Project.objects.filter(dept__name='Tire Building Production').count(),
        'MT':Project.objects.filter(dept__name='Maintenance').count(),
        'CMP':Project.objects.filter(dept__name='Curing & Mold Production').count(),
    }
        st = request.GET.get('state')#REQUEST.GET.GET OLANLARIN HEPSİ HTML'DE GİRİLEN VERİYİ ALİYOR
        st2 = request.GET.get('state-dup')#REQUEST.GET.GET OLANLARIN HEPSİ HTML'DE GİRİLEN VERİYİ ALİYOR
        aim = request.GET.get('aim')#REQUEST.GET.GET OLANLARIN HEPSİ HTML'DE GİRİLEN VERİYİ ALİYOR
        state = Project.objects.filter(year__name=str(st))
        state2 = Project.objects.filter(year__name=str(st2))
        #121den 246ya kadar olan her şey aynı Function,operation ve kullanıcının girdiği yıl filtrelemesi hepsi ondan sonra seçilen filtrelerde indexler hesaplanıyor
        pivot = request.GET.get('pivot')#REQUEST.GET.GET OLANLARIN HEPSİ HTML'DE GİRİLEN VERİYİ ALİYOR
        eng = Project.objects.filter(function__name='Engineering',operation__name='Data Input',year__name=str(pivot))
        eng_c = Project.objects.filter(function__name='Engineering',operation__name='2C',year__name=str(pivot))
        eng_m = Project.objects.filter(function__name='Engineering',operation__name='Measurement',year__name=str(pivot))
        eng_d = Project.objects.filter(function__name='Engineering',operation__name='Decision',year__name=str(pivot))
        eng_a = Project.objects.filter(function__name='Engineering',operation__name='Analysis',year__name=str(pivot))
        eng_o = Project.objects.filter(function__name='Engineering',operation__name='Other',year__name=str(pivot))
        eng_r = Project.objects.filter(function__name='Engineering',operation__name='Reporting',year__name=str(pivot))
        eng_input=0
        for e in eng:
            eng_input = eng_input + e.index
        eng_cc = 0
        for e in eng_c:
            eng_cc = eng_cc + e.index
        eng_meas = 0
        for e in eng_m:
            eng_meas = eng_meas + e.index
        eng_dec = 0
        for e in eng_d:
            eng_dec = eng_dec + e.index
        eng_an = 0
        for e in eng_a:
            eng_an = eng_an + e.index
        eng_oth = 0
        for e in eng_o:
            eng_oth = eng_oth + e.index
        eng_rep = 0
        for e in eng_r:
            eng_rep = eng_rep + e.index
        eng_total = round(eng_rep + eng_oth + eng_dec + eng_meas + eng_cc + eng_input + eng_an)
        pro = Project.objects.filter(function__name='Production', operation__name='Data Input',year__name=str(pivot))
        pro_c = Project.objects.filter(function__name='Production', operation__name='2C')
        pro_m = Project.objects.filter(function__name='Production', operation__name='Measurement',year__name=str(pivot))
        pro_d = Project.objects.filter(function__name='Production', operation__name='Decision',year__name=str(pivot))
        pro_a = Project.objects.filter(function__name='Production', operation__name='Analysis',year__name=str(pivot))
        pro_o = Project.objects.filter(function__name='Production', operation__name='Other',year__name=str(pivot))
        pro_r = Project.objects.filter(function__name='Production', operation__name='Reporting',year__name=str(pivot))
        pro_input = 0
        for e in pro:
            pro_input = pro_input + e.index
        pro_cc = 0
        for e in pro_c:
            pro_cc = pro_cc + e.index
        pro_meas = 0
        for e in pro_m:
            pro_meas = pro_meas + e.index
        pro_dec = 0
        for e in pro_d:
            pro_dec = pro_dec + e.index
        pro_an = 0
        for e in pro_a:
            pro_an = pro_an + e.index
        pro_oth = 0
        for e in pro_o:
            pro_oth = pro_oth + e.index
        pro_rep = 0
        for e in pro_r:
            pro_rep = pro_rep + e.index
        pro_total = round(pro_rep + pro_oth + pro_dec + pro_meas + pro_cc + pro_input + pro_an)
        tech = Project.objects.filter(function__name='Technology', operation__name='Data Input',year__name=str(pivot))
        tech_c = Project.objects.filter(function__name='Technology', operation__name='2C',year__name=str(pivot))
        tech_m = Project.objects.filter(function__name='Technology', operation__name='Measurement',year__name=str(pivot))
        tech_d = Project.objects.filter(function__name='Technology', operation__name='Decision',year__name=str(pivot))
        tech_a = Project.objects.filter(function__name='Technology', operation__name='Analysis',year__name=str(pivot))
        tech_o = Project.objects.filter(function__name='Technology', operation__name='Other',year__name=str(pivot))
        tech_r = Project.objects.filter(function__name='Technology', operation__name='Reporting',year__name=str(pivot))
        tech_input = 0
        for e in tech:
            tech_input = tech_input + e.index
        tech_cc = 0
        for e in tech_c:
            tech_cc = tech_cc + e.index
        tech_meas = 0
        for e in tech_m:
            tech_meas = tech_meas + e.index
        tech_dec = 0
        for e in tech_d:
            tech_dec = tech_dec + e.index
        tech_an = 0
        for e in tech_a:
            tech_an = tech_an + e.index
        tech_oth = 0
        for e in tech_o:
            tech_oth = tech_oth + e.index
        tech_rep = 0
        for e in tech_r:
            tech_rep = tech_rep + e.index
        tech_total = round(tech_rep + tech_oth + tech_dec + tech_meas + tech_cc + tech_input + tech_an)
        cto = Project.objects.filter(function__name='Vice CTO', operation__name='Data Input',year__name=str(pivot))
        cto_c = Project.objects.filter(function__name='Vice CTO', operation__name='2C',year__name=str(pivot))
        cto_m = Project.objects.filter(function__name='Vice CTO', operation__name='Measurement',year__name=str(pivot))
        cto_d = Project.objects.filter(function__name='Vice CTO', operation__name='Decision',year__name=str(pivot))
        cto_a = Project.objects.filter(function__name='Vice CTO', operation__name='Analysis',year__name=str(pivot))
        cto_o = Project.objects.filter(function__name='Vice CTO', operation__name='Other',year__name=str(pivot))
        cto_r = Project.objects.filter(function__name='Vice CTO', operation__name='Reporting',year__name=str(pivot))
        cto_input = 0
        for e in cto:
            cto_input = cto_input + e.index
        cto_cc = 0
        for e in cto_c:
            cto_cc = cto_cc + e.index
        cto_meas = 0
        for e in cto_m:
            cto_meas = cto_meas + e.index
        cto_dec = 0
        for e in cto_d:
            cto_dec = cto_dec + e.index
        cto_an = 0
        for e in cto_a:
            cto_an = cto_an + e.index
        cto_oth = 0
        for e in cto_o:
            cto_oth = cto_oth + e.index
        cto_rep = 0
        for e in cto_r:
            cto_rep = cto_rep + e.index
        cto_total = round(cto_rep + cto_oth + cto_dec + cto_meas + cto_cc + cto_input + cto_an)
        inp_total = round(cto_input + tech_input + pro_input + eng_input)
        cc_total = round(cto_cc + tech_cc + pro_cc + eng_cc)
        meas_total = round(cto_meas + tech_meas + pro_meas + eng_meas)
        dec_total = round(cto_dec + tech_dec + pro_dec + eng_dec)
        an_total = round(cto_an + tech_an + pro_an + eng_an)
        rep_total = round(cto_rep + tech_rep + pro_rep + eng_rep)
        other_total = round(cto_oth + tech_oth + pro_oth + eng_oth)
        grand_total=round(cto_total + tech_total + eng_total + pro_total)
        count = 0
        dt = request.GET.get('dt')
        date = Project.objects.filter(date__name__startswith=str(dt)).order_by('date')
        values = []
        for i in date:
            values.append(i.index)
        series = pd.Series(values)
        cumsum = series.cumsum()
        list = [str(st),str(st2)]
        for s in state:
            count = count + s.index
        ct = 0
        for st1 in state2:
            ct = ct + st1.index
        context = {'pivot':pivot,'cumsum':cumsum,'dt':dt,'date':date,'aim':aim,'an_total':an_total,'rep_total':rep_total,'other_total':other_total,'grand_total':grand_total,'inp_total':inp_total,'cc_total':cc_total,'meas_total':meas_total,'dec_total':dec_total,'project':project,'department':department,'dept':dept,'date':date,'state':state,'count':count,'ct':ct,'list':list,'eng':eng,'eng_input':eng_input,'eng_meas':eng_meas, 'eng_an':eng_an, 'eng_oth':eng_oth, 'eng_dec':eng_dec, 'eng_rep':eng_rep, 'eng_cc':eng_cc, 'eng_total':eng_total,'pro_input':pro_input,'pro_meas':pro_meas, 'pro_an':pro_an, 'pro_oth':pro_oth, 'pro_dec':pro_dec, 'pro_rep':pro_rep, 'pro_cc':pro_cc, 'pro_total':pro_total,'tech_input':tech_input,'tech_meas':tech_meas, 'tech_an':tech_an, 'tech_oth':tech_oth, 'tech_dec':tech_dec, 'tech_rep':tech_rep, 'tech_cc':tech_cc, 'tech_total':tech_total,'cto_input':cto_input,'cto_meas':cto_meas, 'cto_an':cto_an, 'cto_oth':cto_oth, 'cto_dec':cto_dec, 'cto_rep':cto_rep, 'cto_cc':cto_cc, 'cto_total':cto_total, 'op':op}
        return render(request, 'base/stat.html', context)
    else:
        return redirect('home')
#ana sayfa ve veritabanı verilerinin yansıtılması
def home(request):
    if request.user.is_authenticated:
        projeler = Project.objects.all().order_by('id','dept')
        projectFilter = ProjectFilter(request.GET,queryset=projeler)#admin kullanıcı için filtreleme
        defaultProject = defaultProjectFilter(request.GET,queryset=projeler)#admin olmayan kullanıcılar için filtreleme
        function = Function.objects.all()
        states = State.objects.all()
        context = { 'states': states,'function':function,'projectFilter':projectFilter,'defaultProject':defaultProject,'projeler':projeler}
        return render(request, 'base/home.html', context)
    else:
        return redirect('login')

def oldStatusPage(request,pk):
    old = oldStatus.objects.filter(project_id = pk)#SECİLEN HEDEFİN PKSİ VE ONA AİT BİLGİLERİ ALİYOR
    project = Project.objects.get(id=pk)
    p = Project.objects.all()
    context={'p':p,'old':old,'obj':project}
    return render(request, 'base/old.html', context)
def export_excel(request):
    #Satır 112-116 arası dosya tipi ve indirilen dosyanın adını belirleme
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Digindex' + \
                                      str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='UTF-8')
    ws = wb.add_sheet('Digindex')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    #COLUMN VERİLERİNİ BELİRLEME
    columns=['Created By','State','Function','Project No','Department','Responsible','Cs or SmartMNF','Operation','Latest Status','Comp.Date','Planned Year','Fraction','Customer','Index','Created Date']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    #ROW VERİLERİNİ BELİRLEME
    rows = Project.objects.all().values_list("host__first_name","state__name","function__name","id","dept__name","dept__resp__first_name","CS_or_SmartMNF__name","operation__name","latestStatus","date__name","year__name","fraction__name","customer__name","index",'created')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response
#proje yaratma kodları
@login_required(login_url='login')
def createProject(request):
    if request.user.is_authenticated:
        form = ProjectForm()
        # yonetici değişkeni girilen hesabın verisini alip proje eklerken direkt girilen hesap olarak sayiyor
        yonetici = Project(host=request.user)
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=yonetici)
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'form': form}
        return render(request, 'base/project_form.html', context)
    else:
        return redirect('/')
#eğer bir kullanıcının departmanı değişirse onu güncellemek için gereken kodlar
@login_required(login_url='login')
def updateUser(request,pk):
    if request.user.is_superuser:
        kullanici = Department.objects.get(id=pk)#seçilen kullanıcı
        form = updateUserForm
        if request.method == 'POST':
            form =updateUserForm(request.POST,instance=kullanici)
            if form.is_valid():
                form.save()
                return redirect('superuser')
        context = {'form':form,}
        return render(request,'base/updateUser.html',context)
    else:
        return redirect('/')
#projeyi güncelleme
@login_required(login_url='login')
def updateProject(request, pk):
    proje = Project.objects.get(id=pk)#tabloda seçilen projeye ait id'yi alma işlemi yapiyor
    form = ProjectForm(instance=proje)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=proje)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/project_form.html', context)
@login_required(login_url='login')
def deleteProject(request, pk):
    if request.user.is_superuser:
        project = Project.objects.get(id=pk)#tabloda seçilen projeye ait id'yi alma işlemi yapiyor
        if request.method == 'POST':
            project.delete()#silme işlemi
            return redirect('home')
        return render(request, 'base/delete.html', {'obj': project})
    else:
        return redirect('/')
#aşağıdakilerin hepsi veritabanında var olan başlıklara veri ekleme için gerekli kodlar
def addColumn(request):
    form = addColumnForm()
    if request.method == 'POST':
        form = addColumnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context  = {'form':form}
    return render(request,'base/add.html',context)
def addResponsible(request):
    form = addResponsibleForm()
    dept = Department.objects.all()
    user = User.objects.all()

    if request.method == 'POST':
        form = addResponsibleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form,'dept':dept,'user':user}
    return render(request, 'base/addResponsible.html', context)
def addPlannedYear(request):
    form = addYearForm()
    if request.method == 'POST':
        form = addYearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addYear.html', context)
def addCSSMART(request):
    form = addMNFForm()
    if request.method == 'POST':
        form = addMNFForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addsmart.html', context)
def addDepartment(request):
    form = addDepartmentForm
    if request.method == 'POST':
        form = addDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addDepartment.html', context)
def addState(request):
    form = addStateForm()
    if request.method == 'POST':
        form = addStateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addstate.html', context)
def addCompletion(request):
    form = addCompletionForm()
    if request.method == 'POST':
        form = addCompletionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addcompletion.html', context)
def addCustomer(request):
    form = addCustomerForm
    if request.method == 'POST':
        form = addCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addcustomer.html', context)
def addOperation(request):
    form = addOperationForm
    if request.method == 'POST':
        form = addOperationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addoperation.html', context)
def addFraction(request):
    form = addFractionForm
    if request.method == 'POST':
        form = addFractionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form': form}
    return render(request, 'base/addfraction.html', context)
def updateWeight(request,pk):
    weight = Weight.objects.get(id=pk)
    form = updateWeightForm(instance=weight)
    if request.method == 'POST':
        form = updateWeightForm(request.POST,instance=weight)
        if form.is_valid():
            form.save()
            return redirect('superuser')
    context = {'form':form}
    return render(request,'base/updateWeight.html',context)

