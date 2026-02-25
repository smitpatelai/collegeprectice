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

print("\nTotal Revenue by Movie:")
print(df.groupby("Movie")["Revenue_Lakhs"].sum())

print("\nTotal Views by Platform:")
print(df.groupby("Platform")["Views_Millions"].sum())

