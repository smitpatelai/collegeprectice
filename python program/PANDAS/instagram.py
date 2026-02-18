import pandas as pd

data ={
    "Users":["Amit","Jigar","Raj","Neha","Karan"],
    "Followers":[3400,2300,1700,1900,2900],
    "Likes":[400,300,100,900,200],
    "Comments":[200,300,88,22,100],
    "Share":[17,28,24,10,23]
}

df = pd.DataFrame(data)
print(df)


print("\n print first two rows:")
print(df.head(2))

print("\n print last three rows:")
print(df.tail(3))

print(df.info())


print("\n print all user names")
print(df["Users"])


print("\n print users along with its followers")
print(df[["Users","Followers","Likes"]])


print("\n print first row using iloc")
print(df.iloc[0])


print("\n print specific row and col data")
print(df.iloc[3,4])   # corrected (column index 5 → 4)


print("\n print specific row and col data")
print(df.iloc[1:3,0:2])


print(df.loc[0,"Likes"])

print(df.loc[1])


print("\n print data where likes>300")
likes_greater300 = df["Likes"] > 300
print(df[likes_greater300])   # corrected


print("\n print data where followers<2000")
followers_less2000 = df["Followers"] < 2000   # corrected
print(df[followers_less2000])


print(df[df["Followers"] < 3000])

filter_data = (df["Followers"] > 2500) & (df["Likes"] > 400)
print(filter_data)

df["Engagment"] = df["Likes"] + df["Comments"] + df["Share"]
print(df)

df["Ratio"] = df["Engagment"] / df["Followers"]
print(df)

print("\n find person who has higher ratio")
print(df["Ratio"].max())

maxratio = df["Ratio"].max()
print(maxratio)

data1 = df[df["Ratio"] == maxratio]
print(data1.iloc[0,0])


df = df.drop("Ratio", axis=1)
print(df)

print(df.sort_values("Followers", ascending=False).head(2))

# corrected (do not overwrite df)
print(df.loc[0,"Followers"] + 200)
