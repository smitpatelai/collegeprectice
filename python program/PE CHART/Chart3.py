import matplotlib.pyplot as plt

internet_hours_weekday = [2, 3, 4, 5, 6, 7]
sleep_quality_weekday = [9, 8.5, 8, 7, 9, 6]

internet_hours_weekend = [3, 4, 5, 6, 7, 8]
sleep_quality_weekend = [9, 8, 7, 6, 5, 4]

plt.scatter(internet_hours_weekday, sleep_quality_weekday, color='green')
plt.scatter(internet_hours_weekend, sleep_quality_weekend, color='blue')

plt.xlabel("Internet Hours")
plt.ylabel("Sleep Quality")
plt.title("Weekdays v/s Weekend Sleep Quality")
plt.grid()
plt.show()
