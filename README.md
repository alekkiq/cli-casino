# CLI Casino

## Table of contents
- [Description](#description)
    - [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Description

A text & keyboard based 'casino' application that runs on the command line. Allows users to play the most simple casino games with play-money. The app also has some other nice features, such as, a dynamic Leaderboard, the possibility to view the player's own Game history and the chance to edit the players own profile information.

### About
This project is part of the first year engineering studies of 4 eager information technology students, more specifically, the Python basics course. The point of the project is to display the skills learned throughout the course in the form of a high quality and maintainable codebase.

## Installation
1. Clone the whole repository locally:

    ```sh
    git clone https://github.com/alekkiq/cli-casino.git
    ```
2. Navigate to the project directory:

    ```sh
    cd path_to_your_instance/cli-casino
    ```
3. Install the required Python dependencies:

    ```sh
    pip install -r pydeps.txt
    ```
4. Create a ```.env``` file based off of ```.env.example``` and add the proper values for your instance.
5. Run the main script with the ```--setup``` argument to run the database setup:

    ```sh
    python main.py --setup
    ```

## Usage

# TODO

## Features

- Simple casino games

    - Dice
    - Roulette
    - Twenty One
    - Slots
- Dynamic Leaderboard
    - Allows the user to choose, what statistic the leaderboard is based on
    - Also allows the user to choose the order (ascending / descending) of the leaderboard
- Authorization
    - Asks the user for their username & password before entering the 'casino'

        - Gets the users profile from the database if a record matches the credidentials
        - A new profile is created if the username does not exist
- Player's game history
    - Each played "hand" or "game" is saved to the database
    - The user can view their own played games at any time
    - Choose how many games to show
- Profile editing
    - Allows the user to edit their own credidentials (username & password)
    - Allows the user to delete their profile and all records from the database