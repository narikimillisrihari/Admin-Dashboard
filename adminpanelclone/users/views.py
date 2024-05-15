from urllib import request
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from users.form import CreateProjectform,Tldbform,EmployeeForm,TlTaskCreationForm
from users.models import Project,Employee,Tldb,TL_Task,EmployeeManager
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import os
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import logging
import datetime


# manager
# manager
# TL
# Tlaccount
# employee
# Employeeaccount
# Create your views here.
file_path = r"c:\Users\Emphyd12178nkum1\Desktop\Project_log.json".format(id=id)


# Ensure the directory exists, create it if it doesn't
os.makedirs(os.path.dirname(file_path), exist_ok=True)
current_datetime = datetime.datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

logger = logging.getLogger('project_logger')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("valid user")
            auth_login(request,user)
            logger.info(f"{username} Login Successfully")
            return redirect(dashboard)
        else:
            print("invalid username")
            logger.info(f"{username} Invalid username and password")
            return redirect(login)

    else:
        return render(request,"loginpage.html")
@login_required(login_url="/main/login/")    
def dashboard(request):
    Tldata=Tldb.objects.all()
    tldata=[str(employee.employee) for employee in Tldata]
    # print(tldata)
    Empdata=Employee.objects.all()
    empdatas=[str(employee.username)for employee in Empdata]
    # print(empdatas)
    logger.info("Dashboard view accessed")
    if request.user.is_authenticated:
        username = request.user.username
        if username=='manager':
            projectdetails=Project.objects.all()
            tldetails=Tldb.objects.all()
            employeedetails=Employee.objects.all()
            logger.info(f"{username}--Manger Dashboard is opened")
            # project_data={
            #     f"{username} Dashboard": f"Welcome to {username}"
            # }
            # with open(file_path, 'a') as json_file:
                
            #     text_data = f"{formatted_datetime}--{username} Dashboard: Welcome to {username}"
            #     json_file.write(text_data)
            #     json_file.write('\n')
                # Add a separator between the text and JSON data
                
                # json.dump(project_data, json_file)
                # json_file.write('\n')
            # # project_details = Project.objects.values_list('project_title', flat=True)
            # projectdata = {
            #     'project_title':"projectdetails.project_title"
            # }
            # json_data = json.dumps(projectdata, cls=DjangoJSONEncoder)
            # logger.info(f'dashboard project data: {json_data}')
            return render(request,'managerdashboard.html',{'username':username,'projectdetails':projectdetails,'tldetails':tldetails,'employeedetails':employeedetails})
        elif username in tldata:
            # employee=Employee.objects.get(username=username)
            tl_employee = Tldb.objects.get(employee__username=username)
            logger.info(f"{username}--Tl Dashboard is opened")

            return redirect('tldashboard', empid=tl_employee.employee.id)

            # return render(request,'tldashboard.html',{'username':username,'Tldata':Tldata})
        elif username in empdatas:
            employee=Employee.objects.get(username=username)
            logger.info(f"{username}--Employee Dashboard is opened")

            # return redirect('tldashboard',empid=employee.id)
            return redirect(employeedashboard,user_id=employee.id)
            
        else:
            return render(request,'sample.html',{'username':username})
    else:
        return render(login)
    
# def log(request,data):
#     username = request.user.username
#     project_data={
#                 f"{username} {data}": f"Welcome to {username}"
#             }
#     with open(file_path, 'a') as json_file:
                
#         text_data = f"{formatted_datetime}--{username} {data}"
#         json_file.write(text_data)
#         json_file.write('\n')
        # Add a separator between the text and JSON data
        # json.dump(project_data, json_file)
        # json_file.write('\n')
def employeedashboard(request,user_id):
    userid=get_object_or_404(Employee,pk=user_id)
    username=userid.username
    employee_project_details = TL_Task.objects.filter(employee_id=user_id)
    # countof_task=TL_Task.objects.count(employee_id=user_id)
    # print(employee_project_details.count())
    return render(request,'employeedashboard.html',{'username':username,'employee_project_details':employee_project_details})
    
def tldashboard(request,empid):
    employeedata=Tldb.objects.get(employee_id=empid)
    print(employeedata.id)
    # tl_add_task_deatils=TL_Task.objects.get(pk=empid)
    # tl_add_task_deatils=TL_Task.objects.all()
    # tl_add_task_deatils=TL_Task.objects.filter(employee_id=employeedata)
    tl_add_task_deatils=TL_Task.objects.filter(Tldb_id=employeedata.id)


    return render(request,'tldashboard.html',{'employeedata':employeedata,'tl_add_task_deatils':tl_add_task_deatils})

# def tltaskcreation(request,projectid):
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
            logger.info(f"TL task is assigned to employee")

            return redirect(dashboard)
    else:
        # fm=TlTaskCreationForm(initial={'project': tl_project_id,'Tldb':tl_id})
        initial_data = {'project': tl_project_id, 'Tldb':tl_project_id_tltable.pk}
        fm = TlTaskCreationForm(initial=initial_data)
        logger.info(f"TL task is trying to assign a task to  employee")

    return render(request,'tltaskcreation.html',{'form':fm})
def tldetails(request,id):
    tl_data=get_object_or_404(Tldb,pk=id)
    return render(request,'tldetails.html',{'tl_data':tl_data})


def tltaskcreation(request, empid):
    tl_name = get_object_or_404(Tldb, employee_id=empid)
    print(tl_name)
    tl_emp_id=tl_name.employee_id
    tl_project_name = tl_name.project_name
    tl_project = get_object_or_404(Project, project_title=tl_project_name)
    print(tl_project)
    print(tl_project.id)
    tl_tldb = get_object_or_404(Tldb, employee_id=tl_emp_id)
    print(tl_tldb)
    # tl_employee = tl_tldb.employee_id
    # print(tl_employee)

    if request.method == "POST":
        fm = TlTaskCreationForm(request.POST)
        if fm.is_valid():
            tltask = fm.save(commit=False)
            tltask.project = tl_project
            tltask.Tldb = tl_tldb
            tltask.save()
            logger.info("TL task is assigned to employee")
            return redirect('dashboard')
    else:
        initial_data = {'project':tl_project, 'Tldb': tl_tldb}
        fm = TlTaskCreationForm(initial=initial_data)
        logger.info("TL task form initialized with initial data")

    return render(request, 'tltaskcreation.html', {'form': fm})



def logut(request):
    username = request.user.username
    # with open(file_path, 'a') as json_file:
                
    #     text_data = f"{formatted_datetime}--{username} Logout succesfully "
    #     json_file.write(text_data)
    #     json_file.write('\n')
    logger.info(f"{username} Logout Successfully")

    logout(request)
    return redirect(login)

def addproject(request):
    if request.method=="POST":
        fm=CreateProjectform(request.POST)
        if fm.is_valid():
            fm.save()
            fm=CreateProjectform()
            logger.info(f"Manger added project succesfully")
    else:
        fm=CreateProjectform
        logger.info(f"manager ready to add project")
    return render(request,'addproject.html',{'form':fm})

def projectdetails(request,id):
    project=get_object_or_404(Project,pk=id)
    print(project)
    logger.info(f"This is specific--{project}  details")

    return render(request,'project.html',{'project':project})

def projectdetails_json(request, id):
    logger = logging.getLogger('project_logger')  # Custom logger name

    project = get_object_or_404(Project, pk=id)
    project_data = {
        'id': project.id,
        'name': project.project_title,
        'description': project.project_description,
        'project_startingdate':project.project_startingdate.strftime("%Y-%m-%d %H:%M:%S"),
        'project_endingdate':project.project_endingdate.strftime("%Y-%m-%d %H:%M:%S"),
        # Add more fields as needed
    }
    # Serialize project data to JSON string
    json_data = json.dumps(project_data, cls=DjangoJSONEncoder)

    # Log JSON data
    logger.info(f'Project data: {json_data}')
    print("log data is added")

    # Specify the custom file path on your local machine
    file_path = r"c:\Users\Emphyd12178nkum1\Desktop\project_{id}.json".format(id=id)


    # Ensure the directory exists, create it if it doesn't
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write project data to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(project_data, json_file)
    print("file is created in dektop")

    return JsonResponse({'message': f'Project data saved to {file_path}'})

def AddTL(request):
    if request.method=="POST":
        fm=Tldbform(request.POST)
        if fm.is_valid():
            fm.save()
            fm=Tldbform()
            logger.info(f"Manger added Tl to specific project")
    else:
        fm=Tldbform
        logger.info(f"Manger Try to adding Tl")
    return render(request,'Tldbform.html',{'form':fm})

def Employeecreation(request):
    if request.method=="POST":
        fm=EmployeeForm(request.POST)
        if fm.is_valid():
            fm.save()
            fm=EmployeeForm()
            logger.info(f"Manger added Employe to specific project")
            return redirect(login)
    else:
        fm=EmployeeForm
        logger.info(f"Manger Trying to add Employe to specific project")

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
    logger.info(f"Manger Deleted project----{item.project_title}")
    item.delete()
    

    return redirect(dashboard)
def employeedata(request,id):
    item=get_object_or_404(Employee,pk=id)
    logger.info(f"Manger Deleted Employee----{item.username}")
    item.delete()
    return redirect(dashboard)
def tldelete(request,id):
    item=get_object_or_404(Tldb,pk=id)
    logger.info(f"Manger Deleted TL----{item.username}")
    item.delete()
    return redirect(dashboard)
def tltaskdata(request,id):
    item=get_object_or_404(TL_Task,pk=id)
    logger.info(f"TL Deleting the task data")
    item.delete()
    return redirect(dashboard)

def sample(request):
    employe_latest_data=EmployeeManager.objects.all()
    return render(request,'sample.html',{'employe_latest_data':employe_latest_data})



# def tlcreateddata(request):
#     TL_Created_Task_data=TL_Task.objects.all()
#     return render(request,'TL_Created_Task_data.html',{'TL_Created_Task_data':TL_Created_Task_data})

# def tlcreateddatadelate(request,id):
#     item=get_object_or_404(TL_Task,pk=id)
#     item.delete()
#     print("item is deleted")
#     return redirect(tlcreateddata)
