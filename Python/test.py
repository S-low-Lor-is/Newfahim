import math
import time
import sys
import grpc
from datetime import datetime
import re
#sys.path.append('E:\Fiverr Workspace\proto environment\Python')

import partner_api2_pb2_grpc as api
from partner_api2_pb2 import *
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
import json
import pytz



#function
def extract_usages (string):
  # Initialize an empty dictionary
  usages_dict = {}
  # Use re.findall to find all the numbers after 'usages:' in the string   r'usages: (\d+\.?\d*)'
  usages_list = re.findall (r'usages: (\d+\.?\d*+)', string)
  # Loop through the usages_list and convert the strings to floats
  for i, usage in enumerate (usages_list):
    # Use the index as the key and the usage as the value in the dictionary
    usages_dict [i+1] = float (usage)
    
  # Return the dictionary
  return usages_dict

def extract_weekday (string):
  # Initialize an empty dictionary
  weekday_dict = {}
  # Use re.findall to find all the numbers after 'usages:' in the string   r'usages: (\d+\.?\d*)'
  #usages_list = re.findall (r'usages: (\d+\.?\d*+)', string)
  weekday_list = re.findall (r'bucket_epoch_seconds: (\d+\.?\d*+)', string)
  # Loop through the usages_list and convert the strings to floats
  for i, usage in enumerate (weekday_list):
    # Use the index as the key and the usage as the value in the dictionary
    weekday_dict [i+1] = int (usage)
    dt = datetime.fromtimestamp( weekday_dict [i+1])
    day_of_week = dt.strftime('%a')
    weekday_dict[i+1]=day_of_week
  # Return the dictionary
  return weekday_dict

def extract_hour (string):
  hour_dict = {}
  hour_list = re.findall (r'bucket_epoch_seconds: (\d+\.?\d*+)', string)
  for i, hour in enumerate (hour_list):
    hour_dict [i+1] = int (hour)
    dt = datetime.fromtimestamp( hour_dict [i+1])
    time_of_hour = dt.strftime('%H:%M')
    hour_dict[i+1]=time_of_hour
  # Return the dictionary
  return hour_dict


# This sub section provide auth token in usable format
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
#This sub section provide auth token in usable format

# get list of devices managed by partner
inventoryRequest = DeviceInventoryRequest()
inventoryRequest.auth_token = auth_token
inventoryResponse = stub.GetDevices(inventoryRequest)
# display device information
print(f'Fahim you  partner account has {len(inventoryResponse.devices)} devices fahimmmmmm associated to it')

#outlet conneted and information about those outlet
devices = inventoryResponse.devices
outlet_list = [dev for dev in devices if dev.model == DeviceInventoryResponse.Device.DeviceModel.Outlet]
print(f'\n***Your partner account has {len(outlet_list)} Outlets associated to it')
if len(outlet_list) > 0:
    outlet = outlet_list[0]
    listDevicesRequest = ListDevicesRequest()
    listDevicesRequest.auth_token = auth_token
    listDevicesRequest.manufacturer_device_ids.append(outlet.manufacturer_device_id)

    listDevicesResponse = stub.ListOutlets(listDevicesRequest)
    first_outlet = listDevicesResponse.outlets[0]

    model = outlet.model

    # print("Here are the details of the first outlet")
    # print(f' Manufacturer Device Id: {outlet.manufacturer_device_id}')
    # print(f'                  Model: {DeviceInventoryResponse.Device.DeviceModel.Name(model)}')
    # print(f'                   Name: {outlet.device_name}')
    # print(f'       Device Connected: {outlet.device_connected}')
    # print(f'              Outlet On: {first_outlet.on}')

    # toggle outlet state
    if outlet.device_connected :
        #print( f'toggling the On/Off for outlet {outlet.manufacturer_device_id}')
        #first_outlet.on = not first_outlet.on
        updateOutletRequest = UpdateOutletsRequest()
        updateOutletRequest.auth_token = auth_token
        updateOutletRequest.outlets.append(first_outlet)
        updateOutletResponse = stub.UpdateOutlets(updateOutletRequest)
        #print( f'updateOutletsResponse indicates the on/off flag is {updateOutletResponse.outlets[0].on}')
    else :
        print( f'Outlet {outlet.manufacturer_device_id} is not connected so we cannot turn it on/off')        

    print(type(first_outlet.on))


#data usages.......for outlet 1 and devices.
# start_epoch_seconds=1699055000
# end_epoch_seconds=1699056000
# scale=2
# channels=1
manufacturer_device_ids=outlet.manufacturer_device_id



data_usage_request=DeviceUsageRequest()
data_usage_request.auth_token=auth_token
sub_three_hours=20*60
sub_day=24*60*60
sub_week=24*60*60*6
sub_month=24*60*60*30
data_usage_request.start_epoch_seconds=int(time.time())-sub_three_hours
data_usage_request.end_epoch_seconds=int(time.time())

data_usage_request.scale=0
data_usage_request.channels=1
#data_usage_request.manufacturer_device_ids= 
data_usage_request.manufacturer_device_ids.append(manufacturer_device_ids)


data_usage_response = stub.GetUsageData(data_usage_request)

#print(data_usage_response.device_usages)

#print(type(data_usage_response.device_usages))


#working fine upto the above
#new try below




data_dick =data_usage_response.device_usages
xx=data_dick.__str__()
print('maybe string version of the xx')
print(type(xx))
print(xx)




# Call the function and print the result
result = extract_usages (xx)
result2=extract_hour(xx)
print (result)
print(result2)
print(type(result))


#data_dict = protobuf_to_dict (data_dick, use_enum_labels=True)

# data_dic = MessageToDict (data_dick, preserving_proto_field_name=True, including_default_value_fields=False)
# print(data_dic)
# Assuming your gRPC data is stored in a variable called data
#json_object = protobuf_to_dict(data_dick) # Convert gRPC message to JSON object
#dictionary = json.loads(json_object) # Convert JSON object to dictionary



#functionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn



