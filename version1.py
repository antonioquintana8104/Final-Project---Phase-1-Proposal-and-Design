# import all of the needed libraries
import pandas as pd
import random
import os
# Variable for the data file name
DATA_FILENAME = "recommendations.csv"

# function to get the path of the database file
def get_database_path(filename=DATA_FILENAME):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)
# Function to validate yes/no input
def validate_yes_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "no", "si"]:
            return "yes" if response in ["yes", "si"] else "no"
        print("Invalid input. Enter yes or no.")

def clean_rating_string(value):
    if pd.isna(value):
        return ""

    if isinstance(value, float) or isinstance(value, int):
        return str(float(value))

    # value is string
    parts = str(value).split(",")
    clean_list = []

    for p in parts:
        p = p.strip()
        if p == "":
            continue
        try:
            clean_list.append(str(float(p)))
        except:
            continue

    return ",".join(clean_list)

# Calculate average rating
def calculate_average_rating(rating_string):
    if rating_string is None or rating_string == "" or pd.isna(rating_string):
        return None, 0
    try:
        parts = [float(x) for x in rating_string.split(",") if x.strip() != ""]
    except:
        return None, 0

    if len(parts) == 0:
        return None, 0

    return sum(parts) / len(parts), len(parts)


# Main functions
def main():

    print("Welcome to the Culture Library, here you can find culturally rich recommendations for music, books, and movies!")

    # Input name
    while True:
        user_name = input("Please enter your name: ").strip()
        if user_name.replace(" ", "").isalpha():
            break
        print("Invalid input. Please enter a valid name (letters only).")

    while True:
        # Load CSV file
        try:
            try:
                df = pd.read_csv(DATA_FILENAME)
            except FileNotFoundError:
                df = pd.read_csv(get_database_path())
        except Exception as e:
            print("Could not load database.csv")
            print("Make sure it is in the SAME folder as this script.")
            print("Details:", e)
            return

        # filter rating column
        df["Rating"] = df["Rating"].apply(clean_rating_string)

        # Ask media type
        while True:
            media_input = input(f"\nHi {user_name}, what type of media? (music/books/movies): ").strip().lower()
            if media_input in ["music", "song"]:
                media_type = "song"
                break
            if media_input in ["books", "book"]:
                media_type = "book"
                break
            if media_input in ["movies", "movie"]:
                media_type = "movie"
                break
            print("Invalid input. Please enter music, books, or movies.")

        want_new = validate_yes_no("Do you want something with no rating yet? (yes/no): ")
        want_specific = validate_yes_no("Do you want to filter by genre? (yes/no): ")
        df["Type of media"] = df["Type of media"].astype(str).str.lower().str.strip()
        filtered = df[df["Type of media"] == media_type]

        # Genre filter
        if want_specific == "yes":
            all_genres = filtered["Genre"].astype(str).str.strip().unique()
            all_genres = [g for g in all_genres if g.lower() != "nan"]

            if len(all_genres) == 0:
                print("No genre data available.")
            else:
                print("\nAvailable genres:")
                genre_dict = {}
                for i, g in enumerate(all_genres, start=1):
                    print(f"{i}. {g}")
                    genre_dict[i] = g
                # Ask the user to choose a genre by number
                while True:
                    try:
                        n = int(input("Choose a genre by its number: "))
                        if n in genre_dict:
                            break
                        print("Invalid number. Please input a number between 1-3.")
                    except:
                        print("Enter a number.")
                genre_choice = genre_dict[n].lower().strip()
                filtered = filtered[filtered["Genre"].astype(str).str.lower().str.strip() == genre_choice]

        if want_new == "yes":
            filtered = filtered[filtered["Rating"] == ""]

        if filtered.empty:
            print("\nNo items match your criteria.")
        else:
            # Randomly select an item
            item = filtered.sample(n=1).iloc[0]
            # Display recommendation
            print("\nRecommendation")
            print("Name:", item["Name"])
            print("Type:", item["Type of media"])
            print("Genre:", item["Genre"])
            print("Description:", item["Description"])
            print("Info:", item["Info"])
            # Show average rating
            avg, count = calculate_average_rating(item["Rating"])
            if avg is not None:
                print(f"Average Rating: {round(avg,2)} ({count} ratings)")
            else:
                print("No ratings yet.")

            # Rating system and validation
            if validate_yes_no("Would you like to rate this item? (yes/no): ") == "yes":
                while True:
                    try:
                        r = float(input("Enter rating (1–5): "))
                        if 1 <= r <= 5:
                            break
                        print("Enter a number between 1 and 5.")
                    except:
                        print("Invalid number. PLease input a valid number.")
                # Update rating in DataFrame
                old = item["Rating"]
                new_rating = str(r)

                if old == "" or pd.isna(old):
                    updated = new_rating
                else:
                    updated = old + "," + new_rating

                df.loc[df["Name"] == item["Name"], "Rating"] = updated
                # Save back to CSV
                try:
                    df.to_csv(DATA_FILENAME, index=False)
                    print("Rating saved!")
                except Exception as e:
                    print("Error saving file:", e)
        # Ask the user if they want another recommendation
        if validate_yes_no("Another recommendation? (yes/no): ") == "no":
            print("Thank you for using the Culture Library. Goodbye!")
            break


if __name__ == "__main__":
    main()
