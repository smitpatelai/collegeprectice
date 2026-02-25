import pandas as pd

data = {
"Movie": ["KGF", "KGF", "KGF", "Pushpa", "Pushpa", "Pushpa",
          "Dangal", "Dangal", "Dangal", "Jawan", "Jawan", "Jawan"],

"Genre": ["Action", "Action", "Action",
          "Action", "Action", "Action",
          "Drama", "Drama", "Drama",
          "Action", "Action", "Action"],

"Platform": ["Netflix", "Amazon", "Hotstar",
             "Netflix", "Amazon", "Hotstar",
             "Netflix", "Amazon", "Hotstar",
             "Netflix", "Amazon", "Hotstar"],

"Year": [2022, 2022, 2022,
         2023, 2023, 2023,
         2021, 2021, 2021,
         2023, 2023, 2023],

"Views_Millions": [25, 20, 15,
                   30, 22, 18,
                   28, 24, 19,
                   35, 26, 21],

"Revenue_Lakhs": [500, 420, 350,
                  600, 480, 390,
                  550, 460, 370,
                  700, 520, 410]
}

df = pd.DataFrame(data)
print(df)

print("\n Total Revenue by Movie")

pivot1 = pd.pivot_table(
    df,
    values="Revenue_Lakhs",
    index="Movie",
    aggfunc="sum"
)

print(pivot1)

print("\n Total Views by Platform")

pivot2 = pd.pivot_table(
    df,
    values="Views_Millions",
    index="Platform",
    aggfunc="sum"
)

print(pivot2)

print("\n Average Revenue per Genre")

pivot3 = pd.pivot_table(
    df,
    values="Revenue_Lakhs",
    index="Genre",
    aggfunc="mean"
)

print(pivot3)

print("\n Total Revenue per Year")

pivot4 = pd.pivot_table(
    df,
    values="Revenue_Lakhs",
    index="Year",
    aggfunc="sum"
)

print(pivot4)

print("\n Total Views per Genre")

pivot5 = pd.pivot_table(
    df,
    values="Views_Millions",
    index="Genre",
    aggfunc="sum"
)

print(pivot5)


print("\n Movies Sorted by Revenue (High to Low)")

pivot6 = pd.pivot_table(
    df,
    values="Revenue_Lakhs",
    index="Movie",
    aggfunc="sum"
)

print(pivot6.sort_values(by="Revenue_Lakhs", ascending=False))


print("\n Platforms Sorted by Views (Low to High)")

pivot7 = pd.pivot_table(
    df,
    values="Views_Millions",
    index="Platform",
    aggfunc="sum"
)

print(pivot7.sort_values(by="Views_Millions", ascending=True))

print("\n Top 3 Highest Revenue Movies")

pivot8 = pd.pivot_table(
    df,
    values="Revenue_Lakhs",
    index="Movie",
    aggfunc="sum"
)

top3 = pivot1.sort_values(by="Revenue_Lakhs", ascending=False).head(3)
print(top3)

print("\n Bottom 2 Movies by Total Views")

pivot9 = pd.pivot_table(
    df,
    values="Views_Millions",
    index="Movie",
    aggfunc="sum"
)

bottom2 = pivot2.sort_values(by="Views_Millions", ascending=True).head(2)
print(bottom2)

print("\n Genres Sorted by Average Revenue")

pivot10 = pd.pivot_table(
    df,
    values="Revenue_Lakhs",
    index="Genre",
    aggfunc="mean"
)

sorted_genre = pivot3.sort_values(by="Revenue_Lakhs", ascending=False)
print(sorted_genre)

