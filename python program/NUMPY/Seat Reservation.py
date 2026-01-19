import numpy as np

# Create bus seating layout: 12 rows, 3 seats per row, 0 = available
bus_seats = np.zeros((12, 3), dtype=int)

# print(bus_seats)
# print("shape:", bus_seats.shape)

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


if __name__ == "__main__":

    bookings = book_random_seats(bus_seats, n=5, seed=42)

    # print("Booked seats (row, col) [0-based]:", bookings)
    print("\nSeating layout (1 = booked, 0 = available):\n", bus_seats)
    print("\nRow booking counts:", bus_seats.sum(axis=1))

