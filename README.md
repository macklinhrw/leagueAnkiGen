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

You can also import the included abilities.txt as a demo. It was generated
a couple months ago, so may not be up to date with mobafire.

# Tags and other features
Each card is tagged and can be searched for in anki. There are two
types of cards right now, one for cooldowns, and one for ability description.

You can sort and suspend the type you don't want to review.

The tags are:

1. `cooldown`

2. `ability`

It's easy to add questions, just go to the end of the file and copy/edit the format I used for the above question types.

# Importing into Anki
Open Anki and go to `File > Import` then select the text file with the
exported abilities.

Change the deck in the top left of the import screen, either select an existing
one or create a new one.

You're ready to go! You can start memorizing abilites now.