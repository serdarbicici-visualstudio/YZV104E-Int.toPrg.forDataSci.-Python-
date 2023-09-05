# Spelling Bee by Serdar Biçici

## Introduction
Spelling Bee is a desktop application. It is a word game designed by the New York Times where players have to form valid words using a set of given letters. The game also provides hints and tracks the player's progress.

## Features
- Randomly generates a set of letters for the player to form words
- Validates the entered word against a dictionary of valid words
- Provides hints for valid words and pangrams
- Tracks the player's progress, including the number of found words and the score
- Allows the player to delete the current word
- Supports extra letter option for additional gameplay however words with extra letter only affects score not game progress
- Displays a progress bar to show the player's progress

## Technologies Used
- Python
- Tkinter: Python's standard GUI library for creating the application's graphical user interface
- Matplotlib: A plotting library used to display a figure with the given letters
- Requests: A library used to send HTTP requests and retrieve data from websites
- BeautifulSoup: A library used for web scraping and extracting data from HTML

## Installation
1. Install the required dependencies: `pip install -r requirements.txt`
4. Run the application: `python main.py`

## How to Play
1. Launch the application by following the installation instructions.
2. The application will display a set of letters. Your goal is to form valid words using these letters.
3. A valid vord consists of at least three letters and it has to contain "middle letter".
4. Click on the letter buttons to create a word. The selected letters will be displayed in the "Enter Word..." label.
5. To delete the current word, click the "Delete" button.
6. Once you have formed a valid word, it will be added to the list of found words.
7. The application provides hints for valid words and pangrams. The hints can be seen in the corresponding labels.
8. The progress bar shows your progress in finding valid words. Once you have found all the valid words, the game is completed.
9. You can save your progress and start a new game by clicking the "SAVE" button and choosing another saved game.

## 	Recommendations
1. In the left side of the game window, there is a dispaly that shows previous found words. By clicking on them users can access their dictionary meaning
2. In order to complete the game you must enter nearly all possible forms of words such as: plural form, -ing form, -ly form etc.
3. To not get any errors use only one window at a time and DO NOT CLOSE the main window.