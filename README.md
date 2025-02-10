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
- `state_bird`: (optional) The official bird for the state
- `popular_food`: (optional) A popular dish for the state

## Program Description
This section describes the main program `query.py`. This file consists of all code for prompting the user for a query,
parsing the query, retrieving data from the database, and returning results to the user. It also contains additional
utilities such as providing help to the user.

### Query Language

This program uses a domain-specific, declarative query language desgined to filter data on U.S. states. It allows users to contruct queries using relational and logical operators to refine search results.

#### Syntax
The query language supports categorical and numerical filtering, as well as compound queries.

#### Fields 
**Categorical fields** (string-based):
- `state`
- `capital`
- `governor`
- `state_bird`
- `popular_food`

**Numerical fields** (integer-based):
- `population`
- `num_counties`
  
(See more about the fields by clicking [here](#our-data))

#### Queries and Operators
| Query Type  | Description | Supported Operators   | Example               | Meaning                                                  |
| ----------- | - | --------------------- | --------------------- | -------------------------------------------------------- |
| Categorical | Simple query that filters by categorical field | ==, !=                | `region == Northeast`   | "All states in the northeast region"                     |
| Numerical   | Simple query that filters by numerical field | ==, !=, <, >, <=, >=  | `population > 10000000` | "All states with a population greater than 10 million"   |
| Compound    | Query that combines multiple simple queries | &&                    | `region == Northeast && population > 10000000` | "All states in the northeast region and with a population greater than 10 million" |

#### Other Language Specifics
- String-based terms with whitespace characters must be enclosed in either a single or double quote
  - Example: `state == New York` or `state == "New York"`
- Language is case insensitive
  - Example: `state == new york` is the same as `state == New York` is the same as `state == NEW YORK`
- Language features simple commands `help`: to display a help menu on how to structure queries, and `exit`: to exit the program



### Functions

- `display_welcome_screen`: Displays a welcome screen to the user with a quick introduction on how to use the program.  
- `display_help_screen`: Displays in-depth instructions on how to structure queries upon user's request
- `program_exit`: Function for exiting the program, confirms with the user prior to exiting
- `validate_and_parse_input`: Parser function that defines all possible queries and commands the user can make,
parses the input, and sends an error message if the user enters a query or command the parser cannot interpret. The parsed input is then formatted and sent to the `query_database` function
- `query_database`: Takes a parsed input and retrieves matching records from the Firestore database and sends the records to the `final_answer` function
- `final_answer`: Processes the data into user-friendly, readable format, and prints the result to the user


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

