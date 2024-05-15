from django.forms import  ModelForm
from users.models import Project,Employee,Tldb,TL_Task
from django.contrib.auth.models import User
from django import forms


class CreateProjectform(ModelForm):
    class Meta():
        model=Project
        fields="__all__"

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    reenter_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['username', 'employee_designation', 'password', 'reenter_password']

    def clean_reenter_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        reenter_password = cleaned_data.get("reenter_password")

        if password and reenter_password and password != reenter_password:
            raise forms.ValidationError("Passwords do not match")

        return reenter_password

    def save(self, commit=True):
        employee = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        if commit:
            # Create a User instance associated with the employee
            user = User.objects.create_user(username=username, password=password)
            employee.save()
        return employee


class Tldbform(ModelForm):
    class Meta():
        model=Tldb
        fields="__all__"

class TlTaskCreationForm(ModelForm):
    class Meta():
        model=TL_Task
        fields="__all__"