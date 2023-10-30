from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Master
from datetime import datetime

class CreateTask(APIView):
    def post (self, request):
        result={}
        result['status']="NOK"
        result['valid']=False
        result['result']={"message":"Unauthorized access","data":[]}
        #------------------------------------------------------------------------------------
        try:
            record_object = Master()
            record_object.save()
            id = record_object.id 
            record_object.unique_id = f'task{id + 100000:07d}'
            record_object.description = request.data['description']
            record_object.title = request.data['title']
            record_object.created_timestamp = datetime.today()
            record_object.save()

            query_set = Master.objects.filter(id = id).values()

            result['status']            ="OK"
            result['valid']             = True
            result['result']['message'] = "Created Successfully"
            result['result']['data']    = query_set
            return Response(result, status=status.HTTP_201_CREATED)
        except KeyError as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
      
class UpdateTask(APIView):
    def post (self, request):
        result={}
        result['status']="NOK"
        result['valid']=False
        result['result']={"message":"Unauthorized access","data":[]}
        #------------------------------------------------------------------------------------
        try:
            inp_id      = request.data['id']
            task        = Master.objects.filter(id = inp_id).first()
            if task is not None:
                title       = request.data.get('title', task.title)
                description = request.data.get('description', task.description)
                print(title, description)

                query_set = Master.objects.filter(id = inp_id).update(title = title, description = description)

                result['status']            = "OK"
                result['valid']             = True
                result['result']['data']    = query_set
                result['result']['message'] = "Updated Successfully"
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                result['result']['message'] = "Task with the specified ID not found."
        except KeyError as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
    
class DeleteTask(APIView):
    def post (self, request):
        result={}
        result['status']="NOK"
        result['valid']=False
        result['result']={"message":"Unauthorized access","data":[]}
        #------------------------------------------------------------------------------------
        try:
            inp_id    = request.data['id']
            query_set = Master.objects.filter(id = inp_id).update(status = 0)
            
            result['status']            = "OK"
            result['valid']             = True
            result['result']['data']    =  query_set
            result['result']['message'] = "Updated Successfully"
            return Response(result, status=status.HTTP_201_CREATED)
        except KeyError as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
    
class GetTask(APIView): 
    def get (self, request):
        result={}
        result['status']="NOK"
        result['valid']=False
        result['result']={"message":"Unauthorized access","data":[]}
        #------------------------------------------------------------------------------------
        try:
            query_set = Master.objects.all()

            result['result']['data']    =  query_set
            result['result']['message'] = "Fetchec Successfully"
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
    
class ChangeStatusTask(APIView):
    def post (self, request):
        result={}
        result['status']="NOK"
        result['valid']=False
        result['result']={"message":"Unauthorized access","data":[]}
        #------------------------------------------------------------------------------------
        try:
            inp_id    = request.data['id']
            query_set = Master.objects.filter(id = inp_id, status = 1).update(is_completed = 1)
            
            result['status']            = "OK"
            result['valid']             = True
            result['result']['data']    = query_set
            result['result']['message'] = "Updated Successfully"
            return Response(result, status=status.HTTP_201_CREATED)
        except KeyError as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e :
            result['result']['message'] = "Error due to " + str(e)
            return Response(result, status=status.HTTP_201_CREATED)
        
