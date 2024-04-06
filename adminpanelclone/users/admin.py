from django.contrib import admin

# Register your models here.
from .models import TL_Task,Project,Employee,Tldb


admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Tldb)
admin.site.register(TL_Task)