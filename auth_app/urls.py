from django.urls import path


from auth_app.views import *

urlpatterns = [
    path('sign_up/', sign_up),
    path('login/', log_in),
    path('logout/', log_out),
    path('me/', get_logged_in_user_data),
    path('version/', get_version),
    path("", index)
]