import matplotlib.pyplot as plt

defects = [2, 3, 1, 4, 5, 6, 4, 3, 2, 1, 7, 8, 6, 5, 4, 3, 2, 1, 2, 3]

plt.hist(defects,edgecolor="black",bins=6,color="blue")

plt.xlabel("Defect Count per Day")
plt.ylabel("Frequency")
plt.title("Product Defect Count Distribution")
plt.show()
