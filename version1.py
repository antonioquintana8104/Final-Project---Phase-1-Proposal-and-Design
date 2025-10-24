import pandas as pd
import random

print("Welcome to the Culture Library, here you can find culturally rich recommendations for music, books, and movies!")
while True:
    name = input("Please enter your name: ").strip()
    if name.isalpha():
        break
    else:
        print("Invalid input. Please enter a valid name (letters only).")
while True:
    media = input(f"Hi {name}, what type of media are you interested in? (song/book/movie): ").strip().lower()
    visit = input("Are you interested in something new? (yes/no): ").strip().lower()
    df = pd.read_excel("/Users/antonioquintanarivas/Desktop/final_project/database.xlsx")
    filtered_df = df[df["Type of media"].str.lower() == media]
    if visit == "yes":
        filtered_df = filtered_df[filtered_df["Rating"].isna()]
    else:
        pass
    if filtered_df.empty:
        print(f"Sorry, no {media} met the criteria.")
    else:
        random_row = filtered_df.sample(n=1).iloc[0]
        print("\n Here’s a random recommendation:")
        print(f"\nName: {random_row['Name']}")
        print(f"\nGenre: {random_row['Genre']}")
        print(f"\nDescription: {random_row['Description']}")
        print(f"\nInfo: {random_row['Info']}")
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
            df.loc[df["Name"] == random_row["Name"], "Rating"] = rating
            df.to_excel("/Users/antonioquintanarivas/Desktop/final_project/a01288104.xlsx", index=False)
            print(f"\nRating {rating} saved for {random_row['Name']}")
    another = input("\nWould you like another recommendation? (yes/no): ").strip().lower()
    if another == "yes":
        break
    else:
        print("\nThank you for using the Culture Library. Goodbye!")
