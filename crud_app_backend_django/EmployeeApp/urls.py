from django.urls import re_path
from EmployeeApp import views

urlpatterns = [
    re_path(r'^departments$', views.departmentApi)
]
