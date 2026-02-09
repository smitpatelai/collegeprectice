import matplotlib.pyplot as plt


teenegers = [20,30,40,45,50,55,70,80]
young_adults = [20,130,40,150,50,55,170,80]
adults = [30,40,50,45,55,60,65,90]

age = [teenegers,young_adults,adults]
labels = ["teenagers","young_adults","adults"]
plt.violinplot(age)
plt.legend(labels=labels)
plt.show()