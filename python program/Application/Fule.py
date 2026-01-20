from datetime import datetime

def get_fuel_price(fuel_type):
    price = {
        "petrol": 96,
        "diesel": 90,
        "cng": 80
    }
    return price.get(fuel_type.lower(), 0)


def apply_discount(total_amount):
    now = datetime.now().hour

    if 9 <= now <= 12:
        return total_amount * 0.05   # 5% discount
    elif 21 <= now <= 23:
        return total_amount * 0.03   # 3% discount
    else:
        return 0


def calculate_total_amount(price_per_liter, liters):
    base_amount = price_per_liter * liters
    discount = apply_discount(base_amount)
    final_amount = base_amount - discount

    return base_amount, discount, final_amount


def print_receipt(fuel_type, liters, price_per_liter, discount, final_amount):
    print("\n------------------ PATEL PETROL PUMP ------------------")
    print(f"Fuel Type           : {fuel_type}")
    print(f"Price per Liter     : ₹{price_per_liter}")
    print(f"Fuel Quantity       : {liters} liters")
    print(f"Discount Applied    : ₹{discount:.2f}")
    print(f"Total Payable Amount: ₹{final_amount:.2f}")
    print("------------------------------------------------------")
    print("Thank You for Visiting 🙏")


def main():
    fuel_type = input("What Fuel do you want? : ")
    liters = float(input("How many liters? : "))

    fuel_price = get_fuel_price(fuel_type)

    if fuel_price == 0:
        print("❌ Invalid Fuel Type")
    else:
        base_amount, discount, final_amount = calculate_total_amount(fuel_price, liters)
        print_receipt(fuel_type, liters, fuel_price, discount, final_amount)


main()
