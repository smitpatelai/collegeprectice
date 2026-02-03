import matplotlib.pyplot as plt

brands = ["Samsung","Apple","Xiaomi","OnePluse","Others"]
sales = [12500000,52000000,8900000,5600000,46000000]


plt.pie(sales,labels=brands,autopct="%1.1f",colors=("darkgray","gold","crimson","royalblue","aquamarine"))
plt.show()