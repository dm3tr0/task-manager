from django import forms
from app.models import Task, Project, Type, Status, WorkTime
from authentication.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'type', 'project', 'start', 'end', 'plan_time']
        widgets = {
            'plan_time': forms.TextInput(attrs={
                'placeholder': 'e.g. 2:30:00 (2 hours 30 minutes)',
                'required': 'true',
            }),
            'start': forms.DateInput(attrs={'type': 'date', 'required': 'true'}),
            'end': forms.DateInput(attrs={'type': 'date', 'required': 'true'}),
        }

    name = forms.CharField(
        label="Task name",
        required=False,
        widget=forms.TextInput(attrs={'required': 'true'})
    )

    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.TextInput(attrs={'required': 'true'})
    )

    start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'required': 'true'})
    )

    end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'required': 'true'})
    )

    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        required=False,
        widget=forms.Select(attrs={'required': 'true'})
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={'required': 'true'})
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={'required': 'true'})
    )

    implementer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'required': 'true'})
    )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'blocked']

    name = forms.CharField(label="Name", required=False,
                           widget= forms.TextInput
                           (attrs={
                               'required': 'True'
                            }))

    description = forms.CharField(label="Description", required=False,
                           widget= forms.TextInput
                           (attrs={
                               'required': 'True'
                            }))

class StatusForm(ProjectForm):
    class Meta:
        model = Status
        fields = ['name', 'description', 'blocked']

class TimeRegistrationForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['time', 'description', 'date']
        widgets = {
            'time': forms.TextInput(attrs={'placeholder': 'e.g. 2:30:00 (2 hours 30 minutes)'}),
        }

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    