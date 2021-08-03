from django.urls import path
from .views import auth_views, todo_views, test_views
urlpatterns = [
    path("accounts/register/", auth_views.UserRegisterView.as_view(),
         name="account_register"),
    path("accounts/login/", auth_views.AuthView.as_view(), name="account_login"),
    path("accounts/refresh-token", auth_views.AuthView.as_view(), name="refresh_token"),
    path("todos/", todo_views.TodoListView.as_view(), name="todo_list"),
    path("todos/<int:pk>", todo_views.TodoDetailView.as_view(), name="todo_detail"),
    path("tests/", test_views.TestView.as_view(), name="test_api")
]
