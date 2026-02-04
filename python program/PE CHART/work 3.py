import matplotlib.pyplot as plt

subjects = ["Mathematics", "Science", "English", "History","Geography", "Computer", "Economics", "Arts"]

books_issued = [180, 220, 260, 140, 120, 310, 90, 70]
plt.pie(books_issued,labels=subjects,autopct='%1.1f%%',shadow=True)
plt.xlabel("Subjects And Book Issued")
plt.title("School Library Book Issuance Analysis")
plt.show()
