import matplotlib.pyplot as plt

data = {
    "Hour":[9,10,11,12,13,14,15,16],
    "Heartbit":[25,80,27,98,59,70,91,120]
}

plt.plot(data["Hour"],data["Heartbit"],color="red",marker="*")
plt.xlabel("Hour")
plt.ylabel("Heartbit")
plt.title("Heart Reate of Patients")
plt.show()
