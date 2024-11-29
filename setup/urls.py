from django.contrib import admin
from django.urls import path, include
from todos.views import (
    TodoListView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    TodoLoginView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", TodoLoginView.as_view(), name="login"),
    path("", TodoLoginView.as_view(), name="login"),
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo_update"),
    path("todos/<int:pk>/delete/", TodoDeleteView.as_view(), name="todo_delete"),
    path("todo_list/", TodoListView.as_view(), name="todo_list"),
]
