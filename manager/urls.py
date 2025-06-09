from django.urls import path, include
from app import views  # type: ignore
from app.views import TaskList, ProjectList, TypeList, StatusList, EventList
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:id>/", views.task_detail, name="task_detail"),
    path("<str:id>/edit/", views.edit_task, name="task_edit"),
    path("<str:id>/register_time/", views.register_time, name="register_time"),
    path("<str:id>/delete/", views.delete_task, name="task_delete"),
    path("task_list", TaskList.as_view(), name="task_list"),
    path("add_task", views.add_task, name="add_task"),
    path("project_list", ProjectList.as_view(), name="project_list"),
    path("type_list", TypeList.as_view(), name="type_list"),
    path("status_list", StatusList.as_view(), name="status_list"),
    path("event_list", EventList.as_view(), name="event_list"),
    path("add_project", views.add_project, name="add_project"),
    path("add_status", views.add_status, name="add_status"),
    path("add_type", views.add_type, name="add_type"),
    path('auth/', include('authentication.urls', namespace='auth')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)