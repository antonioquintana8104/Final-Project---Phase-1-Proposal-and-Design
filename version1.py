import pandas as pd
import random
import os

def open_file_function():
    current_directory = os.path.dirname(__file__)
    file = os.path.join(current_directory, "database.xlsx")
    return file

print("Welcome to the Culture Library, here you can find culturally rich recommendations for music, books, and movies!")

# Ask for and validate user name
while True:
    name = input("Please enter your name: ").strip()
    if name.replace(" ", "").isalpha():
        break
    else:
        print("Invalid input. Please enter a valid name (letters only).")

# Main program loop
while True:
    # Ask for type of media
    media = input(f"\nHi {name}, what type of media are you interested in? (song/book/movie): ").strip().lower()

    # Ask if they want something new
    visit = input("Are you interested in something new? (yes/no): ").strip().lower()

    # Ask if they want specific genre recommendations
    specific = input("Would you like a more specific recommendation? (yes/no): ").strip().lower()

    # Load the Excel database
    df = pd.read_excel(open_file_function())

    # If they want something specific
    if specific == "yes":
        # Get genres available for the selected media
        available_genres = df[df["Type of media"].astype(str).str.lower().str.strip() == media]["Genre"].unique()

        if len(available_genres) == 0:
            print("\nSorry, no genre information is available for this media type.")
            # Default filtering (no genre filter)
            filtered_df = df[df["Type of media"].astype(str).str.lower().str.strip() == media]

        else:
           print("\nAvailable genres:")
           genre_dict = {} 

           for i, g in enumerate(available_genres, start=1):
             print(f"{i}. {g}")
             genre_dict[i] = g

        # Ask user for a number
        while True:
            try:
                choice_num = int(input("\nEnter the number of the genre you want: "))
                if choice_num in genre_dict:
                    break
                else:
                    print("Please choose a valid number.")
            except ValueError:
                print("Invalid input. Enter a number.")

        genre_choice = genre_dict[choice_num].lower().strip()

        # Filter by media AND genre
        filtered_df = df[
            (df["Type of media"].astype(str).str.lower().str.strip() == media) &
            (df["Genre"].astype(str).str.lower().str.strip() == genre_choice)
       ]
    else:
        # No specific genre requested → normal filter by media only
        filtered_df = df[df["Type of media"].astype(str).str.lower().str.strip() == media]

    # If they want something new (unrated)
    if visit == "yes":
        filtered_df = filtered_df[filtered_df["Rating"].isna()]
    # Load the Excel database
    df = pd.read_excel(open_file_function())

    # Filter by type of media
    filtered_df = df[df["Type of media"].astype(str).str.lower().str.strip() == media]

    # If they want something new, filter to items with no rating
    if visit == "yes":
        filtered_df = filtered_df[filtered_df["Rating"].isna()]

    # If there are no results, notify the user
    if filtered_df.empty:
        print(f"\nSorry, no {media} met the criteria.")
    else:
        # Pick one random recommendation
        random_row = filtered_df.sample(n=1).iloc[0]

        # Display all information
        print("\nHere's a random recommendation:")
        print(f"\nName: {random_row['Name']}")
        print(f"Genre: {random_row['Genre']}")
        print(f"Description: {random_row['Description']}")
        print(f"Info: {random_row['Info']}")

        # Show average rating if available
        ratings = random_row["Rating"]
        if pd.notna(ratings):
            rating_list = [float(r.strip()) for r in str(ratings).split(",") if r.strip()]
            avg_rating = sum(rating_list) / len(rating_list)
            print(f"\nAverage rating: {round(avg_rating, 2)} ({len(rating_list)} ratings)")
        else:
            print("\nNo ratings yet.")

        # Ask if the user wants to rate
        rate = input("\nWould you like to rate this recommendation? (yes/no): ").strip().lower()
        if rate == "yes":
            while True:
                try:
                    rating = float(input("Enter your rating (1–5): "))
                    if 1 <= rating <= 5:
                        break
                    else:
                        print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Get the current ratings (if any)
            current_ratings = df.loc[df["Name"] == random_row["Name"], "Rating"].values[0]

            # Append or create new ratings list
            if pd.isna(current_ratings):
                new_ratings = str(rating)
            else:
                new_ratings = f"{current_ratings},{rating}"

            # Save back to DataFrame
            df.loc[df["Name"] == random_row["Name"], "Rating"] = new_ratings

            # Save updated file
            df.to_excel(open_file_function(), index=False)
            print(f"\nYour rating of {rating} has been added for {random_row['Name']}.")

    # Ask if the user wants another recommendation
    another = input("\nWould you like another recommendation? (yes/no): ").strip().lower()
    if another != "yes":
        print("\nThank you for using the Culture Library. Goodbye!")
        break
