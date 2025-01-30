"""
#TODO
Validation function (reuse one from past assignments (?)
Def process_input(string input) -> processed input
Def input_validation(processed_input) -> True/False and error message if false
Def parse_input(validated input) -> parsed language (like the logic operators) / instructions
Def query_database(instructions) -> answer to specific keyword value, makes calls to firebase
Def final_answer(value_from_keyword) -> final answer
"""

from sre_parse import State
import pyparsing as pp
from prettytable import PrettyTable
import json
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter


class StateQueryEngine:
    def display_welcome_screen(self):
        border = "\n" + "*" * 20 + "\n"
        print(border + "Welcome" + border)
        print("These are the things that you can find: \n")
        print("\t1. Capital")
        print("\t2. Population")
        print("\t3. Region")
        print("\t4. Governor")
        print("\t5. Number of Counties")
        print("\t6. Popular dish")
        print("\t7. National Bird")
        print("\t8. Help")

    def program_exit(self):  #REVISIT LATER --> we should show this after user types "exit"
        print("\nAre you sure you want to exit? (y/n)")
        quit_choice = input(">>> ")

        while quit_choice.lower() != "y" and quit_choice.lower() != "n":
            print("\nInvalid option.\n")
            print("Are you sure you want to exit? (y/n)")
            quit_choice = input(">>> ")
        if quit_choice.lower() == "y":
            print("\nThank you for using the top secret system.")
            sys.exit()
        else:
           # reprompt
            pass

    def display_help_screen(self):
        print("this will be the help screen")

        ## explain the format of 'keyword' 'operator' 'value'

        keyword_table = PrettyTable(["Keywords", "Example Query", "Example Return"])
        keyword_table.add_row(["region", ">>> region == northeast", "connecticut, maine, etc."])
        keyword_table.add_row(["info_of", ">>> info_of == vermont", "region, capital, etc."])
        keyword_table.add_row(["capital", ">>> capital == montpelier", "vermont"])
        keyword_table.add_row(["governor", ">>> governor == 'phil scott'", "vermont"])
        keyword_table.add_row(["population", ">>> population > 30000000", "california, texas"])
        keyword_table.add_row(["num_counties", ">>> num_counties > 150", "texas, georgia"])
        keyword_table.add_row(["pop_food", ">>> pop_food == 'boiled peanuts'", "alabama"])
        keyword_table.add_row(["bird", ">>> bird == hermit thrush", "vermont"])

        print(keyword_table)

        logic_table = PrettyTable(["Logic Operators", "Example Query", "Example Return"])
        logic_table.add_row([])

        print(logic_table)


    def validate_and_parse_input(self, user_input):
        """
        Validates and parses the user's input into a list of tokens

        params: query - the user's query
        returns: The parsed user's query OR error message if query is entered incorrectly
        """

        # Define possible tokens
        region = pp.Literal("region")
        info = pp.Literal("info_of")
        population = pp.Literal("population")
        capital = pp.Literal("capital")
        governor = pp.Literal("governor")
        counties = pp.Literal("counties")
        food = pp.Literal("food")
        bird = pp.Literal("bird")
        exit = pp.Literal("exit")
        help = pp.Literal("help")

        numerical_op = pp.oneOf("!= == >= <= > <")
        categorical_op = pp.oneOf("!= ==")

        string = pp.Word(pp.alphas) | pp.QuotedString('"') | pp.QuotedString("'")
        integer = pp.Word(pp.nums)

        region_query = region + categorical_op + string
        info_query = info + categorical_op + string
        population_query = population + numerical_op + integer
        county_query = counties + numerical_op + integer
        capital_query = capital + categorical_op + string
        governor_query = governor + numerical_op + string
        food_query = food + numerical_op + string
        bird_query = bird + numerical_op + string

        single_query = (
                region_query
                | population_query
                | county_query
                | capital_query
                | governor_query
                | food_query
                | bird_query
        )

            # region == Northeast && population > 1000000 &&
            # region == && population > 1000000
            #sublist = [["region", "==", "&&"]]

        query_parser = pp.delimitedList(single_query, delim="&&")


        try:
                # Format list into nested list of single queries for compound quereies
            tokens_list = query_parser.parse_string(user_input, parse_all=True)
                # tokens_ list =  , "population" ...]
            result = []
            while tokens_list:
                query = tokens_list[:3] # query = ["region", "==", "Northeast"]
                result.append(query)
                tokens_list = tokens_list[3:]
            #result =  [["region", "==", "Northeast"], ["population", ">", "100000"]]
            self.query_database(result)

        except pp.ParseException:
            print("Error. Could not parse input. Type 'help' for more information.")

    def query_database(self, parsed_query):
        """
        Makes a call to the firestore database to retrieve specific records
        associated with the input

        params: parsed_query - the parsed user's query
        returns:
        """
        if not firebase_admin._apps:
            cred = credentials.Certificate('path/to/private-key.json')
            firebase_admin.initialize_app(cred)

        # Connect to Firestore DB
        db = firestore.client()

        filtered_docs = []
        for subquery in parsed_query:
            try:
                if isinstance(subquery[3], str):
                    subquery[3].capitalize()
                docs = (
                    db.collection("us_states_data")
                    .where(filter=FieldFilter(subquery[0], subquery[1], subquery[2]))
                    .stream()
                )
            except Exception:
                print("Could not retrieve data for your query. Type 'help' for more information.")

            for doc in docs:
                filtered_docs.append(doc.to_dict())

        return self.final_answer(filtered_docs)


    def final_answer(self, records):
        """
        Processes the data into user-friendly, readable format and prints it to the console

        params:
        returns:
        """
        print("records")

    def main(self):

        self.display_welcome_screen()

        exit_program = False
        while not exit_program:
            user_query = input("> ").strip()

            if user_query.lower() == "exit":
                self.program_exit()

            #process_input = user_query.strip().lower()
            validate_and_parse = self.validate_and_parse_input(user_query)

            print(validate_and_parse)

if __name__ == "__main__":
    engine = StateQueryEngine()
    engine.main()


'''
def validate_input(user_input):

    valid = True
    # Checking if user's input is valid
    keywords = ["population", "counties", "region", "info_of", "capital", "governor", "food", "bird", "exit", "help"]
    operations = ["!=", "==", ">=", "<=", ">", "<"]

    # splitting input into a list
    split_input = (user_input.strip().lower()).split()
    print(split_input)

    if split_input[0] == "exit":
        print("exit ok")
 
    elif split_input[0] == "help":
        print("help ok")

    elif len(split_input) < 3:
        print("Invalid input")
 
        return False
    
    i = 0
    while i < len(split_input):
        keyword = split_input[i]
        operator = split_input[i+1]
        val = split_input[i+2]

        # check if the input contains the allowed keywords and operators
        if keyword not in keywords and operator not in operations:
            print("\nInvalid keyword.\n")
            valid = False

        if keyword == "counties" or keyword == "population":
            if val.isdigit() == False:
                print("Invalid")
                valid = False
        else:
            if val.isalpha() == False:
                print("Invalid")
                valid = False

        # Add 3 to i --> this is because the compound query structure is
        # (keyword, operator, value)  operator  (keyword, operator, value)
       
       if len(split_input) % 3 == 0 or len(split_input) % 3 == 1:
        i += 3 

        # If there are more tokens, they should be logical operators
        if i < len(split_input):
            if split_input[i] != 'and' and split_input[i] != 'or':
                return False
            i += 1  # Move past logical operator

        else:
            print ("incomplete")
    if not valid:
        print ("not valid input")
    else:
        print("valid")
        print(len(split_input) % 3)

validate_input("region == north")
validate_input("region == north and counties > 3 ") 

'''

# def validate_input(user_input):
#
#     valid = True
#     # Checking if user's input is valid
#     keywords = ["population", "counties", "region", "info_of", "capital", "governor", "food", "bird", "exit",
#                 "help"]
#     operations = ["!=", "==", ">=", "<=", ">", "<"]
#
#     # splitting input into a list
#     split_input = (user_input.strip().lower()).split()
#
#     nested_lists_input = []
#     temp_list = []
#     i = 0
#
#     while i < len(split_input):
#         if split_input[i] == '&&':
#             nested_lists_input.append(temp_list)
#             nested_lists_input.append([split_input[i]])
#             temp_list = []
#         else:
#             temp_list.append(split_input[i])
#
#         i += 1
#
#     if temp_list:
#         nested_lists_input.append(temp_list)
#
#     # Check to see that query is "complete"
#     for list in nested_lists_input:
#         for i in range(len(list)):
#
#
#     print(nested_lists_input) #DELETE LATER
#
#     if split_input[0] == "exit":
#         print("exit ok")
#
#     elif split_input[0] == "help":
#         print("help ok")
#
#     elif len(split_input) < 3:
#         print("Invalid input")
#
#         return False
#
#     i = 0
#     while i < len(split_input):
#         keyword = split_input[i]
#         operator = split_input[i + 1]
#         val = split_input[i + 2]
#
#         # check if the input contains the allowed keywords and operators
#         if keyword not in keywords and operator not in operations:
#             print("\nInvalid keyword.\n")
#             valid = False
#
#         if keyword == "counties" or keyword == "population":
#             if val.isdigit() == False:
#                 print("Invalid")
#                 valid = False
#         else:
#             if val.isalpha() == False:
#                 print("Invalid")
#                 valid = False
#
#         # Add 3 to i --> this is because the compound query structure is
#         # (keyword, operator, value)  operator  (keyword, operator, value)
