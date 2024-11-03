from django.shortcuts import render
from .models import student
from .serializers import StudentSerializer 
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
import io
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def studentGet(request):
    if request.method=='GET':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythonData=JSONParser().parse(stream)
        id=pythonData.get('id',None)
        if id is not None:
            stu=student.objects.get(id=id)
            serializer=StudentSerializer(stu)
            json_data=JSONRenderer().render(serializer.data)
            return HttpResponse(json_data,content_type='application/json')
        
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')


    # Handling GET request to retrieve all students
    # if request.method == 'GET':
    #     stu = student.objects.all()  # Get all student records
    #     serializer = StudentSerializer(stu, many=True)  # Serialize all records
    #     json_data = JSONRenderer().render(serializer.data,safe=False)  # Render the serialized data as JSON
    #     return HttpResponse(json_data, content_type='application/json')
    
    # Handling POST request to create a new student record
    
    if request.method == 'POST':
        json_data = request.body  # Read the body of the request
        stream = io.BytesIO(json_data)  # Convert body to a stream
        pythonData = JSONParser().parse(stream)  # Parse the stream to get Python data
        serializer = StudentSerializer(data=pythonData)  # Deserialize the data
        
        if serializer.is_valid():
            serializer.save()  # Save the student if data is valid
            res = {'msg': "Data created successfully"}
            json_data = JSONRenderer().render(res)  # Render success message as JSON
            return HttpResponse(json_data, content_type='application/json')
        
        # Return validation errors if data is invalid
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')
    
    if request.method=='PUT':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythonData=JSONParser().parse(stream)
        id=pythonData.get('id')
        stu=student.objects.get(id=id)
        serializer=StudentSerializer(stu,data=pythonData)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'data updated'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')
    if request.method=='DELETE':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythonData=JSONParser().parse(stream)
        id=pythonData.get('id')

        stu=student.objects.get(id=id)
        stu.delete()
        res={'msg':"data deleted"}
        json_data=JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json')
    json_data=JSONRenderer().render(serializer.errors)
    return HttpResponse(json_data,content_type='application/json')
        

