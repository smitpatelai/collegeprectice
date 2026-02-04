import matplotlib.pyplot as plt

experience = [1, 2, 3, 4, 5, 6, 7, 8]
salary = [25000, 28000, 32000, 36000, 41000, 47000, 53000, 60000]

plt.plot(experience, salary, marker='o')
plt.xlabel("Experience (Years)")
plt.ylabel("Salary")
plt.title("Experience vs Salary")
plt.show()
