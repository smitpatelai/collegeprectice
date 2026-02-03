import matplotlib.pyplot as plt

days = ["mon","tue","wed","thur","fri","sat","sun"]
amd_temp = [45,58,50,25,65,46,20]
del_temp = [45,28,50,20,15,36,30]
jam_temp = [10,15,10,10,22,12,33]

plt.plot(days,amd_temp,marker="+",color="brown",label="Ahmedabad")
plt.plot(days,del_temp,marker="*",linestyle=":",color="red",label="Delhi")
plt.plot(days,jam_temp,marker="o",linestyle="-.",color="green",label="Jamnagar")
plt.xlabel("Days")
plt.ylabel("Temperature")
plt.legend()
plt.show()
