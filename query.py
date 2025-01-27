'''
#TODO
Validation function (reuse one from past assignments (?)
Def process_input(string input) -> processed input
Def input_validation(processed_input) -> True/False and error message if false
Def parse_input(validated input) -> parsed language (like the logic operators) / instructions
Def query_database(instructions) -> answer to specific keyword value, makes calls to firebase
Def final_answer(value_from_keyword) -> final answer
'''

from sre_parse import State
import pyparsing as pp
import json
import sys
import firebase_admin
from firebase_admin import credentials, firestore

class Query:
    REGION_QUERY = 1,
    INFO_QUERY = 2,
    POPULATION_QUERY = 3,
    COUNTY_QUERY = 4,
    CAPITAL_QUERY = 5,
    GOVERNOR_QUERY = 6,
    FOOD_QUERY = 7,
    BIRD_QUERY = 8

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

    def parse_input(self, validated_input):
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
        keywords = [region, info, capital, governor, population, counties, food, bird, exit, help]

        numerical_op = pp.oneOf("!= == >= <= > <")
        categorical_op = pp.oneOf("!= ==")

        string = pp.Word(pp.alphas)
        integer = pp.Word(pp.nums)

        region_query = region + categorical_op + string
        population_query = population + numerical_op + integer
        county_query = counties + numerical_op + integer
        capital_query = capital + categorical_op + string
        governor_query = governor + numerical_op + string
        food_query = food + numerical_op + string
        bird_query = bird + numerical_op + string

        single_query = region_query | population_query | county_query | capital_query | governor_query | food_query | bird_query
        compound_query_and = pp.delimitedList(single_query, delim=["&&", "||"])

        # words = pp.oneOf(keywords)
        # question = words + commands + (integer | words) + pp.Optional(commands + words + commands + (integer | words))

        # test = question
        # queries = ["Region == Northeast", "Population > 1000000", "info_of == Vermont", "Population > 1000000 && Region == Northeast"]
        #
        # for test_str in queries:
        #     try:
        #         testing = test.parseString(test_str)
        #         print(testing)
        #     except pp.ParseException as e:
        #         print("Error: ", e)

    def query_database(self, parsed_query):
        """
        Makes a call to the firestore database to retrieve specific records
        associated with the input

        params: parsed_query - the parsed user's query
        returns:
        """
        # TODO: use parsed input to call firestore database
        cred = credentials.Certificate('path/to/private-key.json')
        firebase_admin.initialize_app(cred)

        # Connect to Firestore DB
        db = firestore.client()

        doc_ref = db.collection("us_states_data").document("name")
        doc = doc_ref.get()

        if doc.exists:
            print(f"Document data: {doc.to_dict()}")
        else:
            print("Document does not exist")

    def final_answer(self, records):
        """
        Processes the data into user-friendly, readable format and prints it to the console

        params:
        returns:
        """

    def main(self):

        self.display_welcome_screen()

        exit = False
        while not exit:
            user_query = input("> ")
            validate_and_parse = self.parse_input(self)

        return

if __name__ == "__main__":
    engine = StateQueryEngine()
    engine.main()