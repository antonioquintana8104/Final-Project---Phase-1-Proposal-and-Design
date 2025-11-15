# Final-Project---Phase-1-Proposal-and-Design
The Culture Library is an interactive Python program designed to provide culturally rich recommendations across different types of media: songs, books, and movies. Its purpose is to promote cultural content at a time when digital platforms increasingly prioritize engagement-based algorithms rather than cultural value.

The program allows the user to select the type of media they are interested in, request recommendations that match a specific genre, choose whether they want new (unrated) content, view cultural descriptions and additional information, and submit their own ratings to help improve future suggestions.
The program uses the external CSV file "recommendations.csv" which must be downloaded before running the program. This CSV file contains information from the recommendations such as name, type of media, genre, description, cultural information, and user ratings.
This project demonstrates how curated cultural content can be made accessible through filtering, interactivity, and dynamic feedback from users.

To run the program you will need **Python 3.8** or any higher version.
The program uses the pandas library which is used to read and write the CSV database, filter data by media type, genre, and rating, and update rating values from user input; the os library which is used for obtaining the correct file path for the database regardless of environment; and the random library which is used for selecting a random recommendation from the filtered dataset.
The pandas library must be downloaded in order to run the program as it does not come preinstalled. To install it you will need to run the following command in the terminal. For Windows run "py -m pip install pandas openpyxl", and for macOS run "python3 -m pip install pandas openpyxl".
To run the program you need to download the Python file named "version1.py" and the CSV file named "recommendations.csv" and place them in the same folder.
