import numpy as np

#1d
#2d
#2d --> MASKING , CONDITIONS , REPLACEMENT


emp_name = np.array(["em1", "em2", "em3", "em4", "em5", "em6", "em7"])
salaries = np.array([20000,50000,44000,30000,40000,27000,36000])
experience = np.array([1,3,2,2,4,5,3])

print("Salaries",salaries)
print("Experience",experience)

#BOOLEAN MASKING ---> use all logical operator like >,<,==,<=,>=,!=

#highest salary
print("Highest Salary",np.max(salaries))

#print salary >30000

high_salary = salaries[salaries>=30000]
print ("Salary >30000",high_salary)

#print salary <30000

low_salary = salaries[salaries<30000]
print ("Salary <30000",low_salary)

#print salary = 20000

exact_salary = salaries[salaries==20000]
print (len(exact_salary))

#multiple condition

eligible_for_promotion = salaries[(salaries>30000) & (experience>3)]
print("People Eligible for promotion",eligible_for_promotion)

# bonus --> 30000> (5000), leser - 2000

bonus = np.where(salaries>30000,5000,2000)
print("Bonus Data",bonus)

#updated_ salary -- <30000 to all salary 30000

updated_salary = np.where(salaries<30000,30000,salaries)
print("updated_salary",updated_salary)

# update salary -- < 30000 to all salary 30000

updated_salary = np.where(salaries<30000,30000,salaries)
print("Updated Salary",updated_salary)


finalsalary = salaries+bonus
print("Final Salary",finalsalary)


# total employee
print("Total Employee",salaries.size)


# top index of highest paid employee
print("Index",np.argmax(salaries))

data = salaries[(salaries>=25000) & (salaries<=45000)]
print("Data",data)
print(np.argmax(data))

