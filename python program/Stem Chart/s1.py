import matplotlib.pyplot as plt

#hours ->orders

hours = [9,10,11,12,13,14,15]
orders = [30,50,90,25,189,141,30]

plt.figure(figsize=(12,6))
plt.stem(hours,orders)
plt.xlabel("Hours")
plt.ylabel("Orders")
plt.title("Hours Orders")
plt.show()