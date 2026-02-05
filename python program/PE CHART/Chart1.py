import matplotlib.pyplot as plt

study_hours = [2,3,4,5,6,7,8]
exam_score = [60,40,58,75,98,98,39]

plt.scatter(study_hours,exam_score)
plt.grid()
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.title("Exam Score v/s Study Hours")
plt.show()
