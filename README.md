# Introduction
This project is a tool to scrape League of Legends abilities from the mobafire database,
as well as turning those abilities into flashcards in a file that can be imported into
Anki.

# Setup
1. Find your Anki collection directory and link paste it into `ANKI_COLLECTION_PATH` in main.py.
2. Install chromedriver and paste the path into `CHROMEDRIVER_PATH`.
3. (optional) Change the filename in the variable `FILENAME`.

# Use
To run the script simply run:

`python main.py`

You can also import the included abilities.txt for as a demo. It was generated
a couple months ago, so may not be up to date with mobafire.