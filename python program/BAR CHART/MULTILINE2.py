import matplotlib.pyplot as plt

subject =["maths","physics","c","c++","Python"]
student1 = [90,55,63,46,45]
student2 = [50,75,63,60,54]
student3 = [60,45,43,56,40]

plt.plot(subject,student1,marker="o",label="Mr.Patel",color="brown")
plt.plot(subject,student2,marker="*",label="Mr.Jamen",color="red")
plt.plot(subject,student3,marker="*",label="Mr.Jamen",color="green")
plt.legend()
plt.show()
