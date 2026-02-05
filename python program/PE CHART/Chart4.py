import matplotlib.pyplot as plt

internet_hours = [2,3,4,5,6,7,8]
productivity = [20,93,46,50,69,75,84]
stress_level = [90,80,70,60,75,80]


plt.scatter(internet_hours,productivity,color='red',alpha=1)

plt.xlabel("Internet Hours")
plt.ylabel("Productivity")
plt.grid()
plt.show()
