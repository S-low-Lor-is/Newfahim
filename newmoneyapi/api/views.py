from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BubbleDataRequestSerializer
from .models import BubbleDataRequestGraph
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from datetime import date, timedelta
from datetime import datetime
from pytz import timezone

#grpc import
import math
import time
import sys
import grpc
sys.path.append('E:\Fiverr Workspace\proto environment\Python')
import partner_api2_pb2_grpc as api
from partner_api2_pb2 import *
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
import json
import re
from .models import Email_Set_Device
#function for finding device model using email,
def your_view_function(request):
    try:
        email_set_device = Email_Set_Device.objects.get(email=request)
        device_model = email_set_device.device_model
        return HttpResponse(f"Device model for {email_to_check}: {device_model}")

    except Email_Set_Device.DoesNotExist:
        # Handle the case where the object is not found
        # You can return a default value or any specific response
        return HttpResponse(f"No device found for {email_to_check}")




class BubbleDataRequestView(APIView):
    def post(self, request):
        data = request.data
        
        serializer = BubbleDataRequestSerializer(data=data)
        #newcode
        mail=data['user_name'] #this is actually email.
        type_of_plot=data['type_of_graph']

        #type_of_plot = data.get('type_of_graph', '')  # Get the value with a default of an empty string

        try:
            # Try to convert 'type_of_plot' to an integer
            type_of_plot = int(type_of_plot)
        except (ValueError, TypeError):
            # Handle the case where the conversion fails (e.g., due to null or blank value)
            type_of_plot = 0
        print('Type of ploooooooooooooooooooooooooooooooooooooooooooooooooooooooooo send by client')
        print(type_of_plot)








        if Email_Set_Device.objects.filter(email=mail).exists(): 
            obj=Email_Set_Device.objects.get(email=mail)
            device_model=obj.device_model
            print(device_model)
            #What if the wrong devic model is entered is not considered
            if len(device_model)<=3:
               return HttpResponse("No no devices for this user is registered the admin panel please contact with the authority")
        else :
           return HttpResponse("User is not  registered")
        #newcodeend

        partnerApiEndpoint = 'partner.emporiaenergy.com:50052'  # this is the V2 of the Partner API
        creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(partnerApiEndpoint, creds)
        stub = api.PartnerApiStub(channel)
        request = AuthenticationRequest()
        request.partner_email = 'hello@newmoney.eco'
        request.password = 'Newmoney!'
        auth_response = stub.Authenticate(request=request)
        auth_token = auth_response.auth_token
        #print(auth_token)
        
        # #This below code is working 
        # inventoryRequest = DeviceInventoryRequest()
        # inventoryRequest.auth_token = auth_token
        # inventoryResponse = stub.GetDevices(inventoryRequest)

        # devices = inventoryResponse.devices
        # outlet_list = [dev for dev in devices if dev.model == DeviceInventoryResponse.Device.DeviceModel.Outlet]
        # if len(outlet_list) > 0:
        #     outlet = outlet_list[1]
        
        # manufacturer_device_ids=outlet.manufacturer_device_id
        # #This above code is working


        data_usage_request=DeviceUsageRequest()
        data_usage_request.auth_token=auth_token

        sub_three_hours=4*60*60
        sub_day=24*60*60
        sub_week=24*60*60*9
        sub_month=24*60*60*30
        scale=1
        if(type_of_plot==0):
           sub=sub_three_hours
           scale=1

        else:
           sub=sub_week
           scale=3

        data_usage_request.start_epoch_seconds=int(time.time())-sub
        data_usage_request.end_epoch_seconds=int(time.time())
        data_usage_request.scale=scale
        data_usage_request.channels=1
        data_usage_request.manufacturer_device_ids.append(device_model)
        # #data_usage_request.manufacturer_device_ids= 
        #data_usage_request.manufacturer_device_ids.append(manufacturer_device_ids) 

        data_usage_response = stub.GetUsageData(data_usage_request)
        data_dick =data_usage_response.device_usages
        xx=data_dick.__str__()
        print('maybe string version of the xx')
        print(type(xx))
        print(xx)
        result = extract_usages (xx)
        weekdays=extract_weekday(xx)
        hours=extract_hour(xx)

        print('this is the hour dictionary provided by the emporia api')
        print(hours)
        # print (result)
        # print(type(result))
        #instead the below code simply i can subtract 1 from the
        # if len(result)==7:
        #    cnt=6
        # else :
        #    cnt=7
        cnt=len(result)-1
        print(cnt)
        print(len(hours))
        print(len(result))
        print('the above value is count')
        if len(result)==0:
           my_dict = []
        elif (type_of_plot==1):
           my_dict = [
                        {
                        "day":weekdays[cnt],
                        "val": result[cnt],
                        "sortingvalue":0
                        },
                        {
                        "day":weekdays[cnt-1],
                        "val": result[cnt-1],
                        "sortingvalue":1
                        },
                       {
                           "day":weekdays[cnt-2],
                        "val": result[cnt-2],
                        "sortingvalue":2
                       },
                       {
                           "day":weekdays[cnt-3],
                        "val": result[cnt-3],
                        "sortingvalue":3
                       },
                        {"day":weekdays[cnt-4],
                        "val": result[cnt-4],
                        "sortingvalue":4
                        },
                        {
                           "day":weekdays[cnt-5],
                        "val": result[cnt-5],
                        "sortingvalue":5
                        },
                        {
                           "day":weekdays[cnt-6],
                        "val":result[cnt-6],
                        "sortingvalue":6
                        },
                        
            ]
        else:
           my_dict = [
                        {
                        "day":hours[cnt],
                        "val": result[cnt],
                        "sortingvalue":0
                        },
                        {
                        "day":"",
                        "val": result[cnt-1],
                        "sortingvalue":1
                        },
                       {
                           "day":"",
                        "val": result[cnt-2],
                        "sortingvalue":2
                       },
                       {
                           "day":hours[cnt-3],
                        "val": result[cnt-3],
                        "sortingvalue":3
                       },
                        {"day":"",
                        "val": result[cnt-4],
                        "sortingvalue":4
                        },
                        {
                           "day":"",
                        "val": result[cnt-5],
                        "sortingvalue":5
                        },
                        {
                           "day":hours[cnt-6],
                        "val":result[cnt-6],
                        "sortingvalue":6
                        },
                        {
                           "day":"",
                        "val":result[cnt-7],
                        "sortingvalue":7
                        },
                        {
                           "day":"",
                        "val":result[cnt-8],
                        "sortingvalue":8
                        },
                        {
                           "day":hours[cnt-9],
                        "val":result[cnt-9],
                        "sortingvalue":9
                        },
  
                        
            ]














        if serializer.is_valid():
            serializer.save()
            return JsonResponse(my_dict, status=status.HTTP_201_CREATED,safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        machine = BubbleDataRequestGraph.objects.all()
        serializer = BubbleDataRequestSerializer(machine, many=True)
        return Response(serializer.data)
    









def extract_usages (string):
  usages_dict = {}
  usages_list = re.findall (r'usages: (\d+\.?\d*+)', string)
  for i, usage in enumerate (usages_list):
    usages_dict [i] = float (usage)
  return usages_dict


def extract_weekday (string):
  weekday_dict = {}
  utc_timezone = timezone('UTC')
  weekday_list = re.findall (r'bucket_epoch_seconds: (\d+\.?\d*+)', string)
  for i, usage in enumerate (weekday_list):
    weekday_dict [i] = float (usage)
    dt = datetime.fromtimestamp( weekday_dict [i],tz=utc_timezone)
    day_of_week = dt.strftime('%a')
    weekday_dict[i]=day_of_week
  # Return the dictionary
  return weekday_dict

def extract_hour (string):
  hour_dict = {}
  utc_timezone = timezone('UTC')
  hour_list = re.findall (r'bucket_epoch_seconds: (\d+\.?\d*+)', string)
  for i, hour in enumerate (hour_list):
    hour_dict [i] = int (hour)
    dt = datetime.fromtimestamp( hour_dict [i],tz=utc_timezone)
    time_of_hour = dt.strftime('%H:%M')
    hour_dict[i]=time_of_hour
  # Return the dictionary
  return hour_dict







# start working response
# class BubbleDataRequestView(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = BubbleDataRequestSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             da={"mess":"perw"}
#             my_dict = {
#                         "name": "Bing",
#                         "age": "89",
                      
#                     }
#             return JsonResponse(my_dict, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def get(self, request):
#         machine = BubbleDataRequestGraph.objects.all()
#         serializer = BubbleDataRequestSerializer(machine, many=True)
#         return Response(serializer.data)
#end working response