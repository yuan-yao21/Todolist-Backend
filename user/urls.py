from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/user", views.get_user_info, name="get_user_info"),
    path(
        "api/v1/user/<int:userId>",
        views.get_user_info_by_id,
        name="get_user_info_by_id",
    ),
    path("api/v1/login", views.login, name="login"),
    path("api/v1/logout", views.logout, name="logout"),
    path("api/v1/register", views.register_user, name="register"),
    path("api/v1/update", views.update_user, name="update"),
]
