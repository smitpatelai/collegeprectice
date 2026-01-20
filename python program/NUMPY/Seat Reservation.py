#!/usr/bin/env python3
import numpy as np

def book_random_seats(bus_seats: np.ndarray, n: int = 5, seed: int | None = None) -> list:
    # """
    # Randomly book `n` seats in `bus_seats` in-place.
    # Constraints:
    #   - Only seats with value 0 may be booked.
    #   - No row may contain more than 2 booked seats.
    #   - Each seat may only be booked once.
    # Returns a list of booked (row, col) tuples (0-based indices).
    # """
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
    # Shows row numbers (1-based) and seat labels 1,2,3 for clarity.
    # """
    rows, cols = bus_seats.shape
    seat_labels = [str(i+1) for i in range(cols)]
    print("Visual seating layout (O = available, X = booked):")
    header = "Row  " + " ".join(seat_labels)
    print(header)
    for r in range(rows):
        symbols = [("X" if bus_seats[r, c] == 1 else "O") for c in range(cols)]
        print(f"{r + 1:>3}  " + " ".join(symbols))
    print()

def get_int_input(prompt: str, min_v: int, max_v: int) -> int:
    """Prompt user until a valid integer in [min_v, max_v] is entered."""
    while True:
        try:
            s = input(prompt).strip()
            val = int(s)
            if not (min_v <= val <= max_v):
                print(f"Please enter a number between {min_v} and {max_v}.")
                continue
            return val
        except ValueError:
            print("Invalid input. Enter an integer.")

if __name__ == "__main__":
    # initial bus seating layout: 12 rows, 3 seats per row; 0 = available
    bus_seats = np.zeros((12, 3), dtype=int)

    # Display the initial seating layout before any bookings
    # print("Initial seat layout (before bookings):\n")
    # print_seating_numeric(bus_seats)
    # print_seating_visual(bus_seats)

    # Book 5 random seats (set seed for reproducibility)
    seed = book_random_seats(bus_seats)  # change/remove for different random outcomes
    bookings = book_random_seats(bus_seats, n=5, seed=seed)

    # Display results after random bookings
    # print("After random bookings:\n")
    # print("Booked seats (row, col) [0-based]:", bookings)
    # print()
    # print_seating_numeric(bus_seats)
    # print_seating_visual(bus_seats)
    # print("Row booking counts (number of booked seats per row):")
    # print(bus_seats.sum(axis=1))
    # print()

    # Accept user input for seat selection
    print("Interactive booking: choose a seat to book.")
    row_in = get_int_input("Enter row number (1-12): ", 1, 12) - 1  # convert to 0-based
    col_in = get_int_input("Enter column number (1-3): ", 1, 3) - 1  # convert to 0-based

    # Validate availability and row constraint
    if bus_seats[row_in, col_in] == 1:
        print(f"Seat Row {row_in+1} Column {col_in+1} is already booked.")
    elif bus_seats[row_in].sum() >= 2:
        print(f"Row {row_in+1} already has 2 booked seats; cannot book another in this row.")
    else:
        bus_seats[row_in, col_in] = 1
        print(f"Successfully booked seat Row {row_in+1} Column {col_in+1}.")

    # Show updated layout
    print("\nUpdated seating after your selection:\n")
    print_seating_numeric(bus_seats)
    print_seating_visual(bus_seats)
    print("Updated row booking counts:")
    print(bus_seats.sum(axis=1))

