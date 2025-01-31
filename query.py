

import pyparsing as pp
from prettytable import PrettyTable
import json
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter


class StateQueryEngine:
    def display_welcome_screen(self):
        border = "\n" + "*" * 48 + "\n"
        print(border + "\tWelcome to the State Query Engine" + border)
        print("You can filter your search by the following: \n")
        print("\t1. Capital")
        print("\t2. Population")
        print("\t3. Region")
        print("\t4. Governor")
        print("\t5. Number of Counties")
        print("\t6. Popular dish")
        print("\t7. National Bird")
        print("\nType 'help' to see how to format a query.")

    def program_exit(self):  # REVISIT LATER --> we should show this after user types "exit"
        print("\nAre you sure you want to exit? (y/n)")
        quit_choice = input(">>> ")

        while quit_choice.lower() != "y" and quit_choice.lower() != "n":
            print("\nInvalid option.\n")
            print("Are you sure you want to exit? (y/n)")
            quit_choice = input(">>> ")
        if quit_choice.lower() == "y":
            print("\nThank you for using the State Query System.")
            sys.exit()
        else:
           self.main()

    def display_help_screen(self):
        # explain the format of 'keyword' 'operator' 'value'
        print("\nThe format of the queries you are able to enter is as follows:")
        print(">>> [ keyword ] [ logical operator ] [ value ] \n")

        keyword_table = PrettyTable(
            ["Keywords", "Example Query", "Example Return"])
        keyword_table.add_row(
            ["region", ">>> region == northeast", "connecticut, maine, etc."])
        keyword_table.add_row(
            ["info_of", ">>> info_of == vermont", "region, capital, etc."])
        keyword_table.add_row(
            ["capital", ">>> capital == montpelier", "vermont"])
        keyword_table.add_row(
            ["governor", ">>> governor == 'phil scott'", "vermont"])
        keyword_table.add_row(
            ["population", ">>> population > 30000000", "california, texas"])
        keyword_table.add_row(
            ["num_counties", ">>> num_counties > 150", "texas, georgia"])
        keyword_table.add_row(
            ["popular_food", ">>> popular_food == 'boiled peanuts'", "alabama"])
        keyword_table.add_row(
            ["state_bird", ">>> state_bird == 'hermit thrush'", "vermont"])
        keyword_table.align = "l"
        print(keyword_table)

        logic_table = PrettyTable(
            ["Logic Operators", "Symbol", "Example Query", "Example Return"])
        logic_table.add_row(
            ["greater than", ">", ">>> population > 30000000", "california, texas"])
        logic_table.add_row(
            ["less than", "<", "num_counties < 4", "delaware"])
        logic_table.add_row(
            ["greater than or equal to", ">=", "num_counties >= 250", "texas"])
        logic_table.add_row(
            ["less than or equal to" ,"<=", "population <= 600000", "wyoming"])
        logic_table.add_row(
            ["equal to", "==", "region == northeast", "connecticut, maine, etc."])
        logic_table.add_row(
            ["not equal to", "!=", "state_bird != hermit thrush", "alabama, arkansas, etc."])
        logic_table.add_row(
            ["and", "&&", "capital == montpelier && governor == 'phil scott'", "vermont"])
        logic_table.align = "l"
        print(logic_table)

    def validate_and_parse_input(self, user_input):
        """
        Validates and parses the user's input into a list of tokens

        params: query - the user's query
        returns: The parsed user's query OR error message if query is entered incorrectly
        """

        # Define possible tokens
        region = pp.Literal("region")
        population = pp.Literal("population")
        capital = pp.Literal("capital")
        governor = pp.Literal("governor")
        num_counties = pp.Literal("num_counties")
        popular_food = pp.Literal("popular_food")
        state_bird = pp.Literal("state_bird")
        help = pp.Literal("help")
        exit = pp.Literal("exit")

        numerical_op = pp.oneOf("!= == >= <= > <")
        categorical_op = pp.oneOf("!= ==")

        string = pp.Word(pp.alphas) | pp.QuotedString(
            '"') | pp.QuotedString("'")
        integer = pp.Word(pp.nums)

        # Define possible queries
        region_query = region + categorical_op + string
        population_query = population + numerical_op + integer
        num_counties_query = num_counties + numerical_op + integer
        capital_query = capital + categorical_op + string
        governor_query = governor + numerical_op + string
        food_query = popular_food + numerical_op + string
        bird_query = state_bird + numerical_op + string

        # Build parser
        single_query = (
            region_query
            | population_query
            | num_counties_query
            | capital_query
            | governor_query
            | food_query
            | bird_query
            | help
            | exit
        )
        query_parser = pp.delimitedList(single_query, delim="&&")

        try:
            # Parse query into a list of tokens
            tokens_list = query_parser.parse_string(user_input, parse_all=True)

            # Display help screen on event user types 'help'
            if tokens_list[0] == "help":
                self.display_help_screen()
            
            # Prompt exit on event user types 'exit'
            elif tokens_list[0] == "exit":
                self.program_exit()

            # Format list into nested list of single queries for compound quereies
            result = []
            if len(tokens_list) >= 3:
                while tokens_list:
                    query = tokens_list[:3]
                    result.append(query)
                    tokens_list = tokens_list[3:]

            # Pass nested list of queries to query engine
            self.query_database(result)

        except pp.ParseException:
            # Print error message for when user enters invalid input that parser cannot interpret
            print("Error. Could not parse input.\nType 'help' to see how to properly format a query.")

    def query_database(self, parsed_query):
        """
        Makes a call to the firestore database to retrieve specific records
        associated with the input

        params: parsed_query - the parsed user's query
        returns:
        """
        # Log in to the firebase system
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                'cs3050-warmup-7457f-firebase-adminsdk-fbsvc-998bc9893a.json')
            firebase_admin.initialize_app(cred)

        # Establish connection to Firestore DB
        db = firestore.client()

        # Loop through subqueries in the parsed query, retrieving corresponding documents for each
        doc_sets = [] # List to store retrieved documents
        try:
            for subquery in parsed_query:
                # Convert numbers to int type
                if subquery[2].isnumeric():
                    subquery[2] = int(subquery[2])
                # Capitalize proper nouns
                elif isinstance(subquery[2], str):
                    subquery[2] = subquery[2].title()
                
                # Retrieve documents from the database
                docs = (
                    db.collection("us_states_data")
                    .where(filter=FieldFilter(subquery[0], subquery[1], subquery[2]))
                    .stream()
                )

                doc_set = {}
                for doc in docs:
                    doc_set[doc.id] = doc.to_dict()
                doc_sets.append(doc_set)
            
            # Compute the intersection of the records to satisfy compound quries
            if doc_sets:
                common_doc_ids = set(doc_sets[0].keys())
                for doc_set in doc_sets[1:]:
                    common_doc_ids.intersection_update(doc_set.keys())
                filtered_docs = [doc_sets[0][doc_uuid] for doc_uuid in common_doc_ids]
            else:
                filtered_docs = []

            return self.final_answer(filtered_docs)
        except Exception:
            print("Error. Could not retrieve records from the database.\nType 'help' to see how to properly format a query.")
    

    def final_answer(self, records):
        """
        Processes the data into user-friendly, readable format and prints it to the console

        params:
        returns:
        """
        # TODO: takes dictionary output and converts it to user-friendly, readable format, then prints that.
        print(json.dumps(records, indent=4)) # Temporary

    def main(self):

        self.display_welcome_screen()

        exit_program = False
        while not exit_program:
            user_query = input("> ").strip()

            # process_input = user_query.strip().lower()
            self.validate_and_parse_input(user_query)


if __name__ == "__main__":
    engine = StateQueryEngine()
    engine.main()
