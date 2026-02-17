import pandas as pd

data = [
    ["Available", "Booked", "Available", "Booked", "Available"],
    ["Booked", "Available", "Booked", "Available", "Available"],
    ["Available", "Available", "Booked", "Booked", "Available"],
    ["Available", "Booked", "Available", "Available", "Booked"],
    ["Booked", "Available", "Booked", "Available", "Available"],
    ["Available", "Booked", "Available", "Booked", "Available"],
    ["Available", "Available", "Booked", "Available", "Booked"],
    ["Booked", "Available", "Available", "Booked", "Available"],
    ["Available", "Booked", "Available", "Available", "Booked"]
]

index= ["VIP", "VIP", "VIP", "Premium", "Premium", "Premium","Classic", "Classic", "Classic"]

columns = ["Seat1", "Seat2", "Seat3", "Seat4", "Seat5"]

df = pd.DataFrame(data, index = index, columns = columns)

print("==========================Concert Seating Layout:==========================\n")
print(df)


row = int(input("Enter row number(0-8): "))
seat = int(input("Enter column number(0-4): "))

if df.iloc[row, seat] == "Available":
    print("Seat is Available.")
    confirm = input("Confirm booking? (yes/no): ")

    if confirm == "yes":
        df.iloc[row, seat] = "Booked"
        print("Seat successfully booked!")

else:
    print("Seat is Already Booked!")

available_count = (df == "Available").sum().sum()
booked_count = (df == "Booked").sum().sum()

row_bookings = (df == "Booked").sum(axis=1)
max_booked_row = row_bookings.idxmax()
highest_booked_row_number = row_bookings.values.argmax()

print("\n----- Final Report -----")
print("No of tickets available:", available_count)
print("No of tickets booked:", booked_count)
print("Row where ticket booked:", max_booked_row)
print("Row no where ticket booked highest:", highest_booked_row_number)
print("----------------------------------------------------")

