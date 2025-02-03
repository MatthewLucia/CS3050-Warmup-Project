# State Query Engine
## CS3050
#### Authors: Sasha J. Abuin, Matt Lucia, Alexa Witkin, Owen Milke

## Overview
This is a command-line based program that allows users to access data about U.S. states via queries . The data is stored in a JSON file: `us_states_data.json`, that was uploaded
to a Google Firestore database via Python in our admin file: `admin.py` (More about the data in the ["Our Data"](#our-data) section). The program 
features a custom query language for filtering data. All input and query processing functionality is located within the query program file: `query.py`. 
The custom query that the user provides is processed through two main functions: a parser function `validate_and_parse_input`, and a database
querying function: `query_database`. The parser function uses the [pyparsing](https://pypi.org/project/pyparsing/) module to parse the user's input. 
The database querying function uses the [firebase_admin](https://firebase.google.com/docs/reference/admin/python/firebase_admin) module to connect
for storing and accessing data. ([Click Here](#setup--running-the-program) for information about setting up and running the program).

## Our Data
The data used in this project is sourced from [wikipedia.com](wikipedia.com). We added the data to a JSON file: `us_states_data.json`, and used
the [firebase_admin](https://firebase.google.com/docs/reference/admin/python/firebase_admin) module in python to upload the data from the json
to the database seamlessly. This functionality is located in the admin file: `admin.py`.

Our data contains the following fields:

- `state`: The name of the state
- `capital`: The name of the state's capital city
- `governor`: The name of the current governor of the state
- `population`: The current population of the state
- `num_counties`: The number of counties in the state
- `national_bird`: (optional) The official bird for the state
- `popular_food`: (optional) A popular dish for the state

## Program Description
This section describes the main program `query.py`. This file consists of all code for prompting the user for a query,
parsing the query, retrieving data from the database, and returning results to the user. It also contains additional
utilities such as providing help to the user.

#### Query Language

#### Functions

`display_welcome_screen`


## Setup / Running the Program
To run the program, follow these steps:

Requires Python >= 3.8 (download here if you don't have it: https://www.python.org/downloads/)

1. Download or clone this project directory
2. Open a new terminal window
3. Navigate to this project directory stored locally on your machine
```bash
cd Path/To/Project/Directory
```
4. (optional) - Start a virtual environment 
```bash
python -m venv venv
```
5. Install dependencies stored in `requirements.txt`
```bash
pip install -r requirements.txt
```
6. Run the program
```bash
python query.py
```

