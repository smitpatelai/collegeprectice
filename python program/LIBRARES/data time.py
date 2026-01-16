from datetime import datetime

# now = datetime.now()
# print(now)
# print("Year:"now.year)
# print("Month:"now.month)
# print("Date:"now.day)
#
# specific time 14:30:00


from datetime import time

specific_time = time(9,0)
print(specific_time)
print("Hours:",specific_time.hour)
print("Minutes:",specific_time.minute)
print("Seconds:",specific_time.second)
print("microseconds:",specific_time.microsecond)
