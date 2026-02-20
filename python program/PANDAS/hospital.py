import pandas as pd

df=pd.read_csv("hospital_data_dirty.csv")
print(df)

print(df[["Age","Discharge_Date","Doctor_Assigned"]])

print(df.isnull().sum())

df["Age"] = pd.to_numeric(df["Age"],errors="coerce")
print(df["Age"])

# df["Gender"]=pd.(df["Gender"],errors="coerce")
# print(df["Gender"])

mean_age = df["Age"].mean()
print(mean_age )
df.fillna({"Age":mean_age}, inplace=True)
df.loc[df["Age"] < 0,"Age"] = mean_age
df.loc[df["Age"] > 50, "Age"] = 50
print(df["Age"])

df['Gender'] = df['Gender'].replace(["Unknown"],pd.NA)
df.fillna({"Gender":"Unknown"},inplace=True)
df.loc[df["Gender"]=="Unknown","Gender"]="Male"
print(df["Gender"])

df['Admission_Date'] = df['Admission_Date'].replace('2026-13-01', '13-01-2026')
df["Admission_Date"]=df["Admission_Date"].fillna("01-02-2026")
print(df['Admission_Date'])

df["Discharge_Date"]=df["Discharge_Date"].fillna("02-05-2026")
print(df["Discharge_Date"])

df.fillna({"Doctor_Assigned":"Dr. Patel"},inplace=True)
df.loc[df["Doctor_Assigned"]=="Dr. NULL","Doctor_Assigned"]="Dr. Patel"
print(df["Doctor_Assigned"])
df["Bill_Amount"]=pd.to_numeric(df["Bill_Amount"],errors="coerce")
print(df["Bill_Amount"])

mean_bill = df["Bill_Amount"].mean()
print(mean_bill)
df.fillna({"Bill_Amount":mean_bill},inplace=True)
df.loc[df["Bill_Amount"]<0,"Bill_Amount"]=mean_bill
print(df["Bill_Amount"])

df.fillna({"Payment_Status":"UnPaid"},inplace=True)
df.loc[df["Payment_Status"] == "Completed", "Payment_Status"] = "UnPaid"
print(df["Payment_Status"])

df.fillna({"Name":"Preet"},inplace=True)
print(df["Name"])

df.to_csv("hospital_data_cleaned.csv")
print("Data Stored")