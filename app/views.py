from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Master
from datetime import datetime
from django.db.models import Q
from datetime import datetime, timedelta

def create_response(valid, data, message, status_code):
    return Response({
        'status': 'OK' if valid is "True" else "NOK",
        'valid': valid,
        'result': {'data': data, 'message': message}
    }, status=status_code)

def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class CreateTask(APIView):
    def post (self, request):
        try:
            record_object = Master.objects.create(
                unique_id=f'task{(Master.objects.count()+1) + 100000:07d}',
                description=request.data['description'],
                title=request.data['title'],
                created_timestamp=datetime.today(),
            )
            query_set = Master.objects.filter(id = record_object.id).values()
            print(query_set)

            return create_response(("True" if record_object is 1 else "False"), query_set, "Created Successfully", status.HTTP_200_OK)
        except KeyError as e :
            create_response(False, [], f"Error due to {str(e)}", status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
      
class UpdateTask(APIView):
    def post (self, request):
        try:
            inp_id      = request.data['id']
            task        = Master.objects.filter(id = inp_id).first()
            if task is not None:
                title       = request.data.get('title', task.title)
                description = request.data.get('description', task.description)

                query_set = Master.objects.filter(id = inp_id).update(title = title, description = description, updated_timestamp = datetime.today())

                return create_response(("True" if query_set is 1 else "False"), [], "Updated Successfully", status.HTTP_200_OK)
            else:
                return create_response(False, [], "Task with the specified ID not found.", status.HTTP_400_BAD_REQUEST)
        except KeyError as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteTask(APIView):
    def post (self, request):
        try:
            inp_id    = request.data['id']
            query_set = Master.objects.filter(id = inp_id).update(status = 0, removed_timestamp = datetime.today())
            
            return create_response(("True" if query_set is 1 else "False"), [], "Updated Successfully", status.HTTP_200_OK)
        except KeyError as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class GetTask(APIView): 
    def get (self, request):
        try:
            query_set = Master.objects.all()
            return create_response(True, query_set, "Fetchecd Successfully", status.HTTP_201_CREATED)
        except Exception as e :
            return create_response(False, [], "Error due to " + str(e), status.HTTP_400_BAD_REQUEST)
           
class ChangeStatusTask(APIView):
    def post (self, request):
        try:
            inp_id    = request.data['id']
            query_set = Master.objects.filter(id = inp_id, status = 1).update(is_completed = 1)

            return create_response(("True" if query_set is 1 else "False"), [], ("Updated Successfully" if query_set is 1 else "Error Updating"), status.HTTP_201_CREATED)
        except KeyError as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return create_response(False, [], f"Error due to {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TaskListing (APIView):
    def post (self, request):
        try:
            search_string = request.data.get('search', '')
            start_date    = request.data.get('start_date', '2023-01-01')
            end_date      = request.data.get('end_date', (datetime.today()).strftime('%Y-%m-%d'))
            if not validate_date(start_date):
                return create_response(False, [], "Invalid start date format, valid format yyyy-mm-dd", status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not validate_date(end_date):
                return create_response(False, [], "Invalid start date format, valid format yyyy-mm-dd", status.HTTP_422_UNPROCESSABLE_ENTITY)

            if end_date < start_date:
                return create_response(False, [], "end date should not be less than start date", status.HTTP_422_UNPROCESSABLE_ENTITY)

            end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

            filter_object = Q(title__icontains=search_string) if search_string else Q()
            filter_object = Q(created_timestamp__range=(start_date, end_date))

            queryset = Master.objects.filter(filter_object, status = 1).values()
            return create_response(True, queryset, "Updated Successfully", status.HTTP_201_CREATED)

        except Exception as e :
            return create_response( False, [], "Error due to " + str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)