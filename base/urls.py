from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('register/',views.registerPage,name = "register"),
    path('',views.home,name="home"),
    path('stat/',views.stat,name="stat"),
    path('old/<str:pk>',views.oldStatusPage,name="old"),
    path('create-project/',views.createProject, name="create-project"),
    path('export-excel',views.export_excel, name="export-excel"),
    path('add-column/',views.addColumn,name="add-column"),
    path('add-responsible/',views.addResponsible,name="add-responsible"),
    path('add-department/',views.addDepartment,name="add-department"),
    path('add-year/',views.addPlannedYear,name="add-year"),
    path('add-mnf/',views.addCSSMART,name="add-mnf"),
    path('add-state/',views.addState,name="add-state"),
    path('add-completion/',views.addCompletion,name="add-completion"),
    path('add-customer/',views.addCustomer,name="add-customer"),
    path('add-operation/',views.addOperation,name="add-operation"),
    path('add-fraction/',views.addFraction,name="add-fraction"),
    path('superuser/',views.superUser,name="superuser"),
    path('update-user/<str:pk>/',views.updateUser,name="update-user"),
    path('update-weight/<str:pk>/',views.updateWeight,name="update-weight"),
    path('update-project/<str:pk>/',views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/',views.deleteProject, name="delete-project"),
]