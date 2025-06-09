from django.db import models
from authentication.models import User

class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    blocked = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.id:
            last_task = Project.objects.order_by('-id').first()
            if last_task and last_task.id.startswith('PRJ'):
                last_id = int(last_task.id[3:])
                new_id = f'PRJ{last_id + 1:05d}'
            else:
                new_id = 'PRJ00001'
            self.id = new_id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Type(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            last_task = Type.objects.order_by('-id').first()
            if last_task and last_task.id.startswith('TYP'):
                last_id = int(last_task.id[3:])
                new_id = f'TYP{last_id + 1:05d}'
            else:
                new_id = 'TYP00001'
            self.id = new_id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Status(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            last_task = Status.objects.order_by('-id').first()
            if last_task and last_task.id.startswith('STT'):
                last_id = int(last_task.id[3:])
                new_id = f'STT{last_id + 1:05d}'
            else:
                new_id = 'STT00001'
            self.id = new_id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    class Meta:
        ordering = ['-id']
        
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, related_name='tasks_created')
    implementer = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, related_name='tasks_implemented')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creation = models.DateField()
    start = models.DateField()
    end = models.DateField()
    plan_time = models.DurationField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_constraint=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_constraint=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_constraint=False)

    def save(self, *args, **kwargs):
        if not self.id:
            last_task = Task.objects.order_by('-id').first()
            if last_task and last_task.id.startswith('TSK'):
                last_id = int(last_task.id[3:])  # Extract numeric part
                new_id = f'TSK{last_id + 1:05d}'  # Increment and format
            else:
                new_id = 'TSK00001'  # First entry
            self.id = new_id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.id

class WorkTime(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_constraint=False)
    description = models.CharField(max_length=255)
    creation = models.DateField(auto_now_add=True)
    date = models.DateField()
    time = models.DurationField()

    def save(self, *args, **kwargs):
        if not self.id:
            last_task = WorkTime.objects.order_by('-id').first()
            if last_task and last_task.id.startswith('TTR'):
                last_id = int(last_task.id[3:])
                new_id = f'TTR{last_id + 1:05d}'
            else:
                new_id = 'TTR00001'
            self.id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.time)

class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    date = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_constraint=False, null=True, blank=True)
    worktime = models.ForeignKey(WorkTime, on_delete=models.CASCADE, db_constraint=False, null=True, blank=True)
    type = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.id:
            last_task = Event.objects.order_by('-id').first()
            if last_task and last_task.id.startswith('EVN'):
                last_id = int(last_task.id[3:])
                new_id = f'EVN{last_id + 1:05d}'  
            else:
                new_id = 'EVN00001'
            self.id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        if self.type == "task_created":
            return f"{self.date} | {self.user} created task ({self.task})"
        elif self.type == "time_registred":
            return f"{self.date} | {self.user} register {self.worktime} on task ({self.task})"