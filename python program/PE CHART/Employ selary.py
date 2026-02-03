import matplotlib.pyplot as plt

salary = [10000,21000,35000,50000,46000,58000,90000,87000,65000,54000,85000,100000,120000,160000]


plt.hist(salary,bins=6,color="blue",edgecolor="black")
plt.xlabel("Salary Range")
plt.ylabel("Count of Employee")
plt.title("Salary Distribution")
plt.show()
