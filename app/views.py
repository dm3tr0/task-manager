from django.shortcuts import render, get_object_or_404, redirect
from app.forms import ProjectForm, StatusForm
from app.forms import TaskForm, TimeRegistrationForm
from app.models import Task, Project, Status, Type, WorkTime, Event
from django.utils import timezone
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail


def home(request):
    return render(request, "main.html")


class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'task'
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.filter()
        
        # filters
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        project_filter = self.request.GET.get('project', '')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if project_filter:
            queryset = queryset.filter(project=project_filter)

        # sorting
        sort_by = self.request.GET.get('sort', '')
        if sort_by in ['name', '-name', 'start', '-start']:
            queryset = queryset.order_by(sort_by)
        
        return queryset

    # context for filters
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        return context


class TypeList(ListView):
    model = Type
    paginate_by = 10
    template_name = 'type_list.html'
    context_object_name = 'type'

    def get_queryset(self):
        return Type.objects.all()


class StatusList(ListView):
    model = Status
    paginate_by = 10
    template_name = 'status_list.html'
    context_object_name = 'status'

    def get_queryset(self):
        return Status.objects.all()


class ProjectList(ListView):
    model = Project
    paginate_by = 10
    template_name = 'project_list.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.all()


class EventList(ListView):
    model = Event
    paginate_by = 10
    template_name = 'event_list.html'
    context_object_name = 'event'

    def get_queryset(self):
        return Event.objects.all()


def add_task(request):
    task_form = TaskForm(request.POST)
    context = {
        'task_form' : task_form
    }
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = Task(
                creator = request.user,
                implementer = task_form.cleaned_data.get("implementer"),
                name = task_form.cleaned_data.get("name"),
                description = task_form.cleaned_data.get("description"),
                creation = timezone.now(),
                start = task_form.cleaned_data.get("start"),
                end = task_form.cleaned_data.get("end"),
                project = task_form.cleaned_data.get("project"),
                status = task_form.cleaned_data.get("status"),
                type = task_form.cleaned_data.get("type"),
                plan_time = task_form.cleaned_data.get("plan_time"),
            )

            event = Event(
                task = task,
                user = task.creator,
                date = task.creation.strftime('%Y-%m-%d %H:%M:%S'), 
                type = "task_created"
            )

            send_mail(
                "Вам назначили задачу!",
                f"Вітаю, {task.implementer.first_name}. Задача {task.id} - {task.name}, від {task.start} до {task.end} додана до списку ваших задач.",
                "taskmanager@example.com",
                [task.implementer.email],
                fail_silently=False,
            )

            task.save()
            event.save()
            return redirect('task_list')

    return render(request, "add_task.html", context)


def add_project(request):
    project_form = ProjectForm(request.POST)
    context = {
        'project_form' : project_form
    }
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = Project(
                name = project_form.cleaned_data.get("name"),
                description = project_form.cleaned_data.get("description"),
                )
            project.save()
            return redirect('project_list')

    return render(request, "add_project.html", context)


def add_status(request):
    status_form = ProjectForm(request.POST)
    context = {
        'status_form' : status_form
    }
    if request.method == "POST":
        status_form = StatusForm(request.POST)
        if status_form.is_valid():
            status = Status(
                name = status_form.cleaned_data.get("name"),
                description = status_form.cleaned_data.get("description"),
                )
            status.save()
            return redirect('status_list')

    return render(request, "add_status.html", context)


def add_type(request):
    type_form = ProjectForm(request.POST)
    context = {
        'type_form' : type_form
    }
    if request.method == "POST":
        type_form = ProjectForm(request.POST)
        if type_form.is_valid():
            type = Type(
                name = type_form.cleaned_data.get("name"),
                description = type_form.cleaned_data.get("description"),
                )
            type.save()
            return redirect('type_list')

    return render(request, "add_type.html", context)


def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            event = Event(
                task = task,
                user = request.user,
                date = timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                type = "task_edited"
            )
            event.save()
            return redirect('task_list')
        else:
            print("FORM ERRORS:", task_form.errors)
    else:
        task_form = TaskForm(instance=task)

    return render(request, "task_edit.html", {'task_form' : task_form, 'task' : task})

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    event = Event(
                task = task,
                user = task.creator,
                date = timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                type = "task_deleted"
            )
    task.delete()
    event.save()
    return redirect('task_list')


def register_time(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TimeRegistrationForm(request.POST)
        if form.is_valid():
            work_time = WorkTime(
                description=form.cleaned_data.get("description"),
                time=form.cleaned_data.get('time'),
                task=task,
                creation=timezone.now(),
                user=request.user,
                date=form.cleaned_data.get("date"),
            )
            
            event = Event(
                worktime = work_time,
                task = work_time.task,
                user = work_time.user,
                date = work_time.creation.strftime('%Y-%m-%d %H:%M:%S'),
                type = "time_registred"
            )

            work_time.save()
            event.save()
            print(event)
            return redirect('task_list')
    else:
        form = TimeRegistrationForm()

    return render(request, 'register_time.html', {'form': form, 'task': task})


def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    work_times = WorkTime.objects.filter(task=task)

    paginator = Paginator(work_times, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_detail.html', {'task': task, 'work_times': work_times, 'page_obj': page_obj})
