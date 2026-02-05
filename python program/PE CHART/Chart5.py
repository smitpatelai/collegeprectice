import matplotlib.pyplot as plt

months = ["Jan","Feb","Mar","Apr","May","Jun"]

air_conditioning = [110,120,125,140,160,150]
computers = [210,230,240,250,220,225]
routers = [30,40,50,60,47,58]


units = [air_conditioning,computers,routers]
labels = ["Air Conditioning","Computers","Routers"]

plt.stackplot(months,units,labels=labels,colors=["yellow","red","black"])
plt.xlabel("Months")
plt.ylabel("Units")
plt.title("Air Conditioning")
plt.legend()
plt.show()