from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from users.form import CreateProjectform,Tldbform,EmployeeForm,TlTaskCreationForm
from users.models import Project,Employee,Tldb,TL_Task
from django.shortcuts import get_object_or_404
# manager
# manager
# TL
# Tlaccount
# employee
# Employeeaccount
# Create your views here.
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("valid user")
            auth_login(request,user)
            return redirect(dashboard)
        else:
            print("invalid username")
            return redirect(login)

    else:
        return render(request,"loginpage.html")
    
def dashboard(request):
    Tldata=Tldb.objects.all()
    tldata=[str(employee.employee) for employee in Tldata]
    # print(tldata)
    Empdata=Employee.objects.all()
    empdatas=[str(employee.username)for employee in Empdata]
    # print(empdatas)


    if request.user.is_authenticated:
        username = request.user.username
        if username=='manager':
            projectdetails=Project.objects.all()
            tldetails=Tldb.objects.all()
            employeedetails=Employee.objects.all()
            return render(request,'managerdashboard.html',{'username':username,'projectdetails':projectdetails,'tldetails':tldetails,'employeedetails':employeedetails})
        elif username in tldata:
            employee=Employee.objects.get(username=username)
            return redirect('tldashboard',empid=employee.id)
            # return render(request,'tldashboard.html',{'username':username,'Tldata':Tldata})
        elif username in empdatas:
            employee=Employee.objects.get(username=username)
            # return redirect('tldashboard',empid=employee.id)
            return redirect(employeedashboard,user_id=employee.id)
            
        else:
            return render(request,'sample.html',{'username':username})
    else:
        return render(login)
    
def employeedashboard(request,user_id):
    userid=get_object_or_404(Employee,pk=user_id)
    username=userid.username
    employee_project_details = TL_Task.objects.filter(employee_id=user_id)
    # countof_task=TL_Task.objects.count(employee_id=user_id)
    # print(employee_project_details.count())
    return render(request,'employeedashboard.html',{'username':username,'employee_project_details':employee_project_details})
    
def tldashboard(request,empid):
    employeedata=Tldb.objects.get(employee_id=empid)
    # tl_add_task_deatils=TL_Task.objects.get(pk=empid)
    # tl_add_task_deatils=TL_Task.objects.all()
    # tl_add_task_deatils=TL_Task.objects.filter(employee_id=employeedata)
    tl_add_task_deatils=TL_Task.objects.filter(Tldb_id=empid)



    return render(request,'tldashboard.html',{'employeedata':employeedata,'tl_add_task_deatils':tl_add_task_deatils})

def tltaskcreation(request,projectid):
    print(projectid)
    tl_project_id = get_object_or_404(Project, pk=projectid)
    print(tl_project_id)
    tl_project_id_tltable=get_object_or_404(Tldb,project_name_id=projectid)
    print(tl_project_id_tltable)
    tl_id=tl_project_id_tltable.employee_id
    print(tl_id)

    if request.method=="POST":
        fm=TlTaskCreationForm(request.POST)
        if fm.is_valid():
            tltaskcreation = fm.save(commit=False)
            tltaskcreation.tl_project_id = tl_project_id
            tltaskcreation.tl_id=tl_id
              # Associate the comment with the specific post
            tltaskcreation.save()
            return redirect(dashboard)
    else:
        # fm=TlTaskCreationForm(initial={'project': tl_project_id,'Tldb':tl_id})
        initial_data = {'project': tl_project_id, 'Tldb':tl_id}
        fm = TlTaskCreationForm(initial=initial_data)
    return render(request,'tltaskcreation.html',{'form':fm})



def logut(request):
    logout(request)
    return redirect(login)

def addproject(request):
    if request.method=="POST":
        fm=CreateProjectform(request.POST)
        if fm.is_valid():
            fm.save()
            fm=CreateProjectform()
    else:
        fm=CreateProjectform
    return render(request,'addproject.html',{'form':fm})

def projectdetails(request,id):
    project=get_object_or_404(Project,pk=id)
    print(project)

    return render(request,'project.html',{'project':project})

def AddTL(request):
    if request.method=="POST":
        fm=Tldbform(request.POST)
        if fm.is_valid():
            fm.save()
            fm=Tldbform()
    else:
        fm=Tldbform
    return render(request,'Tldbform.html',{'form':fm})

def Employeecreation(request):
    if request.method=="POST":
        fm=EmployeeForm(request.POST)
        if fm.is_valid():
            fm.save()
            fm=EmployeeForm()
            return redirect(login)
    else:
        fm=EmployeeForm
    return render(request,'EmployeeForm.html',{'form':fm})

def alldata(request):
    employeedata=Employee.objects.all()
    for i in employeedata:
        print(i.username)
    print()
    Tldata=Tldb.objects.all()
    employee_names = [str(employee.employee) for employee in Tldata]
    print(employee_names)
    username="pradeep"
    if username in employee_names:
        print("welocme"+username)
    else:
        print("not working")

    employeeee=Employee.objects.all()
    empdata=[str(employe.username) for employe in employeeee]
    print(empdata)
    projectid=1
    # project_name=Project.objects.get(project_title=projectid)
    # print(project_name)
    projects=Project.objects.all()
    for project in projects:
        if projectid==project.id:
            projectname=project.project_title
    print(projectname)

def projectdelete(request,id):
    item=get_object_or_404(Project,pk=id)
    item.delete()
    return redirect(dashboard)
def employeedata(request,id):
    item=get_object_or_404(Employee,pk=id)
    item.delete()
    return redirect(dashboard)
def tldelete(request,id):
    item=get_object_or_404(Tldb,pk=id)
    item.delete()
    return redirect(dashboard)
def tltaskdata(request,id):
    item=get_object_or_404(TL_Task,pk=id)
    item.delete()
    return redirect(dashboard)



# def tlcreateddata(request):
#     TL_Created_Task_data=TL_Task.objects.all()
#     return render(request,'TL_Created_Task_data.html',{'TL_Created_Task_data':TL_Created_Task_data})

# def tlcreateddatadelate(request,id):
#     item=get_object_or_404(TL_Task,pk=id)
#     item.delete()
#     print("item is deleted")
#     return redirect(tlcreateddata)
