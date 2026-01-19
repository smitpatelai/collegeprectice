import numpy as np

# Create bus seating layout: 12 rows, 3 seats per row, 0 = available
bus_seats = np.zeros((12, 3), dtype=int)

# print(bus_seats)
# print("shape:", bus_seats.shape)

#Implement Random Seat Booking

def book_random_seats(bus_seats: np.ndarray, n: int = 5, seed: int | None = None) -> list:

    rng = np.random.default_rng(seed)
    rows, cols = bus_seats.shape
    booked = []
    attempts = 0
    max_attempts = 10000

    while len(booked) < n and attempts < max_attempts:
        attempts += 1
        r = rng.integers(0, rows)
        c = rng.integers(0, cols)

        if bus_seats[r, c] != 0:
            continue

        if bus_seats[r].sum() >= 2:
            continue

        bus_seats[r, c] = 1
        booked.append((r, c))

    if len(booked) < n:
        raise RuntimeError(
            f"Could not book {n} seats after {max_attempts} attempts. "
            "This may happen if constraints make remaining bookings impossible."
        )

    return booked

def print_seating_numeric(bus_seats: np.ndarray) -> None:
        """Print the raw numeric seating array (0 = available, 1 = booked)."""
        # print("Numeric seating layout (0 = available, 1 = booked):")
        # print(bus_seats)
        # print()

def print_seating_visual(bus_seats: np.ndarray) -> None:
        # """
        # Print a human-friendly visual of the seating layout.
        # Uses 'O' for available (0) and 'X' for booked (1).
        # Shows row numbers (1-based) and seat labels A,B,C for clarity.
        # """
        rows, cols = bus_seats.shape
        seat_labels = [chr(ord('1') + i) for i in range(cols)]
        print("Visual seating layout (O = available, X = booked):")
        header = "Row  " + " ".join(seat_labels)
        print(header)
        for r in range(rows):
            symbols = [("X" if bus_seats[r, c] == 1 else "O") for c in range(cols)]
            print(f"{r + 1:>3}  " + " ".join(symbols))
        print()

if __name__ == "__main__":
    bus_seats = np.zeros((12, 3), dtype=int)

# this line is use for  random seats book for bus booking
    seed = book_random_seats(bus_seats)
    bookings = book_random_seats(bus_seats, n=5, seed=seed)

    print("After random bookings:\n")

    # print()
    print_seating_numeric(bus_seats)
    print_seating_visual(bus_seats)

    print("Row booking counts (number of booked seats per row):")
    print(bus_seats.sum(axis=1))


