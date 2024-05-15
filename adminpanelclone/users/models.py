from django.db import models

# Create your models here.
class Project(models.Model):
    project_title=models.CharField(max_length=250)
    project_description=models.TextField()
    project_startingdate=models.DateTimeField(auto_now_add=True)
    project_endingdate=models.DateTimeField()
    def __str__(self):
        return self.project_title
    
class EmployeeManager(models.Manager):
    def get_queryset(self):
        # Get a queryset of all employees who are not associated with any Tldb instance
        return super().get_queryset().exclude(employee__isnull=False)


class Employee(models.Model):
    username=models.CharField(max_length=250)
    employee_designation=models.CharField(max_length=50)
    password=models.CharField(max_length=30)
    reenter_password=models.CharField(max_length=30)

    objects = EmployeeManager()  # Use the custom manager

    def __str__(self):
        return self.username



class Tldb(models.Model):
    project_name=models.ForeignKey(Project, related_name="project_name",on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee, related_name="employee",on_delete=models.CASCADE)
    employee_experience=models.IntegerField()
    employee_project_allcoateddate=models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Tldb ID: {self.id}"
    def __str__(self):
        return f"{self.employee.username}"


class TL_Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    Tldb = models.ForeignKey(Tldb, related_name="Tldb", on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name="tasks", on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    task_allocated_date = models.DateTimeField(auto_now_add=True)
    task_ending_date = models.DateTimeField()
    STATUS_CHOICES = (
        ('In Progress', 'Assigned'),
        ('Completed', 'Not Assigned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
# class Employee_Sub_Task(models.Model):
#     project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
#     employee = models.ForeignKey(Employee, related_name="tasks", on_delete=models.CASCADE)
#     task_name = models.CharField(max_length=255)
#     task_description = models.TextField()
#     task_allocated_date = models.DateTimeField(auto_now_add=True)
#     task_ending_date = models.DateTimeField()
#     STATUS_CHOICES = (
#         ('In Progress', 'In Progress'),
#         ('Completed', 'Completed'),
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)

#     def __str__(self):
#         return self.name

