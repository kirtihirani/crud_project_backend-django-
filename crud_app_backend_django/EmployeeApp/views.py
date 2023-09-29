from django.shortcuts import render
import pyclamd
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from EmployeeApp.models import Departments,Employees
from EmployeeApp.serializers import DepartmentSerializer,EmployeeSerializer

# from django.core.files.storage

# Create your views here.
@csrf_exempt
def departmentApi(request, id=0):
    if request.method=='GET':
        if id==0:
            departments = Departments.objects.all()
            dept_serializer = DepartmentSerializer(departments,many=True)
            return JsonResponse(dept_serializer.data,safe=False)
        else:
            dept = Departments.objects.get(DepartmentId=id)
            dept_srl = DepartmentSerializer(dept)
            return JsonResponse(dept_srl.data,safe=False)
    elif request.method=='POST':
        dept_data = JSONParser().parse(request)
        dept_serial = DepartmentSerializer(data=dept_data)
        if dept_serial.is_valid():
            dept_serial.save()
            return JsonResponse("Added succefully",safe=False)
        else:
            return JsonResponse("adding data failed",safe=False)
    elif request.method=='DELETE':
        dept = Departments.objects.get(DepartmentId=id)
        dept.delete()
        return JsonResponse("deleted successfully",safe=False)
    elif request.method=='PUT':
         dept = Departments.objects.get(DepartmentId=id)
         deptData = JSONParser().parse(request) 
         dsrl = DepartmentSerializer(dept,data = deptData)
         if dsrl.is_valid():
            dsrl.save()
            return JsonResponse("updated successfully",safe=False) 
         return JsonResponse("failed to update",safe=False) 

@csrf_exempt
def employeeApi(request,id=0):
    if request.method=='GET':
        if(id==0):
            emp = Employees.objects.all()
            emp_srl = EmployeeSerializer(emp,many=True)
            return JsonResponse(emp_srl.data,safe=False)
        else:
            emp = Employees.objects.get(EmployeeId = id)
            emp_srl = EmployeeSerializer(emp)
            return JsonResponse(emp_srl.data,safe=False)
    elif request.method=='POST':
        emp_data = JSONParser().parse(request)
        emp_srl  = EmployeeSerializer(data= emp_data)
        if emp_srl.is_valid():
            emp_srl.save()
            return JsonResponse("data added successfully" , safe=False)
        else:
             return JsonResponse("data addition failed" , safe=False)

    elif request.method=='DELETE':
        emp = Employees.objects.get(EmployeeId = id)
        emp.delete()
        return JsonResponse("deleted successfully",safe=False)
    elif request.method=='PUT':
         dept = Employees.objects.get(DepartmentId=id)
         deptData = JSONParser().parse(request) 
         dsrl = EmployeeSerializer(dept,data = deptData)
         if dsrl.is_valid():
            dsrl.save()
            return JsonResponse("updated successfully",safe=False) 
         return JsonResponse("failed to update",safe=False) 
    
class UploadView(APIView):
    def post(self,request):
        # file = request.data.get('file', None)
        infected_files =[]
        up_file = request.FILES['file']
        
        try:
            cd = pyclamd.ClamdUnixSocket()
        except pyclamd.ConnectionError:
            return JsonResponse({'status':'Error','message':'could not connect to clamav scanner'})
        
        if up_file:
            file_content = up_file.read()
            scan_result = cd.scan_stream(file_content)
        
            if scan_result is not None:
                if scan_result['stream']:
                    return JsonResponse({'status':'infected','message':f'file is infected with {scan_result["stream"]}'})
                else:
                    return JsonResponse({'status':'clean','message':'file is clean'})
            else:
                return JsonResponse({'status':'error','message':'scan failed'})
            
        else:
            return JsonResponse({'message':'file not uploaded'})
       
        # destination = open('/Users/kirtihirani/' + up_file.name, 'wb+')
        # for chunk in up_file.chunks():
        #     destination.write(chunk)
        # destination.close() 
        print(up_file)
        # if up_file:
        #     return Response({"message":"file has received"}, status=200)
        # else:
        #     return Response({"message":"file not received"}, status=400)
    
# /Users/kirtihirani