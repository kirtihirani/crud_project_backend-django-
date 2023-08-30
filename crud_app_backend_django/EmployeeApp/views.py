from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from EmployeeApp.models import Departments,Employees
from EmployeeApp.serializers import DepartmentSerializer,EmployeeSerializer
# from django.core.files.storage

# Create your views here.
@csrf_exempt
def departmentApi(request, id=0):
    if request.method=='GET':
        departments = Departments.objects.all()
        dept_serializer = DepartmentSerializer(departments,many=True)
        return JsonResponse(dept_serializer.data,safe=False)
    elif request.method=='POST':
        dept_data = JSONParser().parse(request)
        dept_serial = DepartmentSerializer(data=dept_data)
        if dept_serial.is_valid():
            dept_serial.save()
            return JsonResponse("Added succefully",safe=False)
        else:
            return JsonResponse("adding data failed",safe=False)

     

    