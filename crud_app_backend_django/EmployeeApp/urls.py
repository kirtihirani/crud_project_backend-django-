from django.urls import re_path
from EmployeeApp import views
from EmployeeApp.views import *

urlpatterns = [
    re_path(r'^departments$', views.departmentApi),
    re_path(r'^departments/([0-9]+)$',views.departmentApi),
    re_path(r'^employees$',views.employeeApi),
    re_path(r'^employees/([0-9]+)$',views.employeeApi),
    re_path(r'^employees/upload/',UploadView.as_view(),name="file_upload")
]
