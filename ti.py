import time
import re
# x=int(time.time())

# sub_day=24*60*60
# sub_week=24*60*60*6
# sub_month=24*60*60*7*30
# print(sub_day)

from datetime import datetime
import pytz
from pytz import timezone
import pytz

# epoch_timestamp = 1699070400
#dt = datetime.fromtimestamp(epoch_timestamp)
# Define the input string

# Import the re module for regular expressions
import re

# Define a function that takes a string as an argument and returns a dictionary

# def extract_usages (string):
#   # Initialize an empty dictionary
#   usages_dict = {}
#   # Use re.findall to find all the numbers after 'usages:' in the string
#   usages_list = re.findall (r'usages: (\d+\.\d+)', string)
#   # Loop through the usages_list and convert the strings to floats
#   for i, usage in enumerate (usages_list):
#     # Use the index as the key and the usage as the value in the dictionary
#     usages_dict [i] = float (usage)
#   # Return the dictionary
#   return usages_dict

# # Call the function and print the result
# result = extract_usages (string)
# print (result)


#print("Date and Time (in local timezone):", dt)



# Create a naive datetime object
dt = datetime(2023, 11, 9, 15, 7, 3)

# Print the naive datetime object
print(dt)
# Output: 2023-11-09 15:07:03

# Localize the naive datetime object to a specific timezone
# For example, Asia/Dhaka
dhaka_tz = timezone('Asia/Dhaka')
dhaka_dt = dhaka_tz.localize(dt)

# Print the localized datetime object
print(dhaka_dt)
# Output: 2023-11-09 15:07:03+06:00

# Convert the localized datetime object to another timezone
# For example, US/Eastern
eastern_tz = timezone('US/Eastern')
eastern_dt = dhaka_dt.astimezone(eastern_tz)

# Print the converted datetime object
print(eastern_dt)
# Output: 2023-11-09 04:07:03-05:00