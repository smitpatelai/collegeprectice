import random
import math
from datetime import datetime

def start_trip():
    start_time = datetime.now()
    distance = random.randint(5, 50)  # km
    return start_time, distance


def apply_surge(current_time):
    hour = current_time.hour

    # Peak Hours
    if 8 <= hour <= 10:
        return 1.5, "Morning Peak"
    elif 10 <= hour <= 12:
        return 1.5, "Afternoon Peak"
    elif 12 <= hour <= 20:
        return 2.0, "Evening Peak"
    else:
        return 1.0, "No Surge"


def calculate_fare(distance, duration, surge_multiplier):
    base_fare = 40
    fare = base_fare + (12 * distance) + (2 * duration)
    total_fare = fare * surge_multiplier
    return math.ceil(total_fare)


def store_trip_log(trip_id, start_time, distance, fare, surge_status):
    with open("trip_logs.txt", "a", encoding="utf-8") as file:
        file.write(
            f"===== SMART RIDE TRIP SUMMARY =====\n"
            f"Trip ID:  {trip_id}\n"
            f"Date:  {start_time.date()}\n"
            f"Time:  {start_time.time().strftime('%H:%M:%S')}\n"
            f"Distance:  {distance} km\n"
            f"Duration:  {duration} minutes\n"
            f"Fare:  ₹{fare}\n"
            f"Surge:  {surge_status}\n"
        )



trip_id = random.randint(1000, 9999)

start_time, distance = start_trip()

duration = random.randint(10, 90)

current_time = datetime.now()
surge_multiplier, surge_status = apply_surge(current_time)

final_fare = calculate_fare(distance, duration, surge_multiplier)

store_trip_log(trip_id, start_time, distance, final_fare, surge_status)

# OUTPUT
print("===== SMART RIDE TRIP SUMMARY =====")
print(f"Trip ID        : {trip_id}")
print(f"Start Time     : {start_time}")
print(f"Distance       : {distance} km")
print(f"Duration       : {duration} minutes")
print(f"Surge Status   : {surge_status}")
print(f"Final Fare     : ₹{final_fare}")
print("Trip logged successfully!")
