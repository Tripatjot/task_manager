from django.urls import path
from .views import CreateTask, UpdateTask, DeleteTask, GetTask, ChangeStatusTask, TaskListing

urlpatterns = [
    path('CreateTask/', CreateTask.as_view()),
    path('UpdateTask/', UpdateTask.as_view()),
    path('DeleteTask/', DeleteTask.as_view()),
    path('GetTask/', GetTask.as_view()),
    path('ChangeStatusTask/', ChangeStatusTask.as_view()),
    path('TaskListing/', TaskListing.as_view()),
]