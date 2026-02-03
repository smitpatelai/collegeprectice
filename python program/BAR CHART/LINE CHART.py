import matplotlib.pyplot as plt

company = ["Jio","Adani","TCS","Zomato","Torrent"]
price =[315,390,2400,1500,460]

plt.plot(company,price,marker="o",linestyle="solid",color="blue")
plt.grid()
plt.show()
