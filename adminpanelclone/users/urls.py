from django.contrib import admin
from django.urls import path,include
from users import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logut, name='logout'),
    path('addproject/',views.addproject, name='addproject'),
    path('projectdetails/<int:id>/',views.projectdetails, name='projectdetails'),
    path('AddTL/',views.AddTL, name="AddTL"),
    path('Employeecreation/',views.Employeecreation, name='Employeecreation'),
    path('alldata/',views.alldata,name='alldata'),
    path('tldashboard/<int:empid>/',views.tldashboard,name='tldashboard'),
    path('tltaskcreation/<int:projectid>/',views.tltaskcreation,name='tltaskcreation'),
    path('employeedashboard/<int:user_id>/',views.employeedashboard, name='employeedashboard'),
    path('projectdelete/<int:id>/',views.projectdelete,name="projectdelete"),
    path('employeedata/<int:id>/',views.employeedata,name="employeedata"),
    path('tltaskdata/<int:id>/',views.tltaskdata,name="tltaskdata"),
    path('tldelete/<int:id>/',views.tldelete,name="tldelete"),


    # path('tlcreateddata/',views.tlcreateddata,name="tlcreateddata"),
    # path('tlcreateddatadelate/<int:id>/',views.tlcreateddatadelate,name='tlcreateddatadelate'),

]
