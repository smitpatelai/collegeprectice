import random
import math
from datetime import datetime, timedelta

def measure_moisture():
    moisture = random.randint(0, 100)

    if moisture < 20:
        status = "Critical"
    elif 20 <= moisture <= 40:
        status = "Low"
    elif 40 < moisture <= 70:
        status = "Optimal"
    else:
        status = "High"

    return moisture, status


def calculate_water_need(current_moisture, target_moisture, field_area):
    if current_moisture >= target_moisture:
        return 0

    water_needed = (target_moisture - current_moisture) * field_area
    return math.floor(water_needed)


def schedule_irrigation(status):
    now = datetime.now()

    if status == "Critical":
        return now.strftime("%Y-%m-%d %H:%M:%S")

    elif status == "Low":
        next_morning = now + timedelta(days=1)
        scheduled_time = next_morning.replace(hour=6, minute=0, second=0)
        return scheduled_time.strftime("%Y-%m-%d %H:%M:%S")

    else:
        return "No Irrigation Needed"


def save_farm_data(date, moisture, water, status):
    with open("irrigation_log.csv", "a") as file:
        file.write(f"{date},{moisture},{water},{status}\n")


FIELD_AREA = 25        # in hectares
TARGET_MOISTURE = 60   # %

today = datetime.now().date()

moisture, status = measure_moisture()
water_needed = calculate_water_need(moisture, TARGET_MOISTURE, FIELD_AREA)
irrigation_time = schedule_irrigation(status)

save_farm_data(today, moisture, water_needed, status)

# OUTPUT
print("===== SMART IRRIGATION REPORT =====")
print(f"Date              : {today}")
print(f"Soil Moisture     : {moisture}%")
print(f"Moisture Status   : {status}")
print(f"Water Required    : {water_needed} liters")
print(f"Irrigation Time   : {irrigation_time}")
print("Record saved successfully!")
