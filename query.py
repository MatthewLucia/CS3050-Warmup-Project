import pyparsing as pp
from prettytable import PrettyTable
import json
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter


class StateQueryEngine:
    # noinspection PyMethodMayBeStatic
    def display_welcome_screen(self):
        border = "\n" + "*" * 48 + "\n"
        print(border + "\tWelcome to the State Query Engine" + border)
        print("You can filter your search by using the following keywords: \n")
        print("\t- State")
        print("\t- Region")
        print("\t- Capital")
        print("\t- Governor")
        print("\t- Population")
        print("\t- Number of Counties")
        print("\t- Popular Food")
        print("\t- State Bird")
        print("\nType 'help' to see examples of queries.")
        print("Type 'exit' to quit the program.")

        print("\nThe format of the queries you are able to enter is as follows:")
        print(">>> [ keyword ] [ logical operator ] [ value ] \n")

    def program_exit(self):
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

    # noinspection PyMethodMayBeStatic
    def display_help_screen(self):
        ## show keywords, and give example queries
        keyword_table = PrettyTable(
            ["Keywords", "Example Query", "Example Return"])
        keyword_table.add_row(
            ["state", ">>> state == vermont", "region, capital, etc."])
        keyword_table.add_row(
            ["region", ">>> region == northeast", "connecticut, maine, etc."])
        keyword_table.add_row(
            ["capital", ">>> capital == montpelier", "vermont"])
        keyword_table.add_row(
            ["governor", ">>> governor == 'phil scott'", "vermont"])
        keyword_table.add_row(
            ["population", ">>> population > 30000000", "california, texas"])
        keyword_table.add_row(
            ["num_counties", ">>> num_counties > 150", "texas, georgia"])
        keyword_table.add_row(
            ["popular_food", ">>> popular_food == 'clam chowder'", "massachusetts"])
        keyword_table.add_row(
            ["state_bird", ">>> state_bird == 'hermit thrush'", "vermont"])
        keyword_table.align = "l"
        print(keyword_table)

        ## show logic operators, and give example queries
        logic_table = PrettyTable(
            ["Logic Operators", "Symbol", "Example Query", "Example Return"])
        logic_table.add_row(
            ["greater than", ">", ">>> population > 30000000", "california, texas"])
        logic_table.add_row(
            ["less than", "<", ">>> num_counties < 4", "delaware"])
        logic_table.add_row(
            ["greater than or equal to", ">=", ">>> num_counties >= 250", "texas"])
        logic_table.add_row(
            ["less than or equal to" ,"<=", ">>> population <= 600000", "wyoming"])
        logic_table.add_row(
            ["equal to", "==", ">>> region == northeast", "connecticut, maine, etc."])
        logic_table.add_row(
            ["not equal to", "!=", ">>> state_bird != hermit thrush", "alabama, arkansas, etc."])
        logic_table.add_row(
            ["and", "&&", ">>> capital == montpelier && governor == 'phil scott'", "vermont"])
        logic_table.align = "l"
        print(logic_table)

        # explain the format of 'keyword' 'operator' 'value'
        print("\nThe format of the queries you are able to enter is as follows:")
        print(">>> [ keyword ] [ logical operator ] [ value ] \n")

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
        state = pp.Literal("state") # doesn't work yet

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
        state_query = state + categorical_op + string

        # Build parser
        single_query = (
            region_query
            | population_query
            | num_counties_query
            | capital_query
            | governor_query
            | food_query
            | bird_query
            | state_query
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
                return

            # Prompt exit on event user types 'exit'
            elif tokens_list[0] == "exit":
                self.program_exit()
                return

            # Format list into nested list of single queries for compound queries
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
        returns: filtered_docs - a dictionary of documents matching the user's query passed to the final_answer function
                 parsed_query - the parsed user's query passed to the final_answer function
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

            # Compute the intersection of the records to satisfy compound queries
            if doc_sets:
                common_doc_ids = set(doc_sets[0].keys())
                for doc_set in doc_sets[1:]:
                    common_doc_ids.intersection_update(doc_set.keys())
                filtered_docs = [doc_sets[0][doc_uuid] for doc_uuid in common_doc_ids]
            else:
                filtered_docs = []

            if filtered_docs == []:
                print("Error reading input. Did you misspell something?")
            else:
                return self.final_answer(filtered_docs, parsed_query)
        except Exception:
            print("Error. Could not retrieve records from the database.\nType 'help' to see how to properly format a query.")

    # noinspection PyMethodMayBeStatic
    def final_answer(self, records, queries):
        """
        Processes the data into user-friendly, readable format and prints it to the console

        params: records - a dictionary of documents matching the user's query
                queries - a formatted list of the user's query
        returns: void
        """
        # Gets the output from a user's query and formats it into a list
        output = json.loads(json.dumps(records))
        output = [list(data.values()) for data in output]

        # Checks the length of the query list and assigns relevant category, operator, and value
        if len(queries) == 1:
            category = queries[0][0]
            operator = queries[0][1]
            value = queries[0][2]
        elif len(queries) > 1:
            category = "compound"
            operator = None
            value = None
        else:
            category = None
            operator = None
            value = None

        # Adds context for the print statement depending on what category of query the user asked
        if category == "state":
            context = "info"
        elif category == "region":
            context = "States in the %s region: \n" % value
        elif category == "capital":
            context = "%s is the capital of: \n" % value
        elif category == "governor":
            context = "%s is the Governor of: \n" % value
        elif category == "population":
            if operator == "==":
                context = f"States with a population of {value:,}: \n"
            elif operator == "!=":
                context = f"States with a population not exactly equal to {value:,}: \n"
            else:
                context = f"States with a population of {'over' if operator in ['>', '>='] else 'less than'} {value:,}: \n"
        elif category == "num_counties":
            if operator == "==":
                context = f"States with exactly {value} counties: \n"
            elif operator == "!=":
                context = f"States that don't have exactly {value} counties: \n"
            else:
                context = f"States with {'over' if operator in ['>', '>='] else 'less than'} %s counties: \n" % value
        elif category == "popular_food":
            context = "States with %s as their popular food: \n" % value
        elif category == "state_bird":
            context = "States with the %s as their state bird: \n" % value
        elif category == "compound":
            context = "States that satisfy all queries: \n"
        else:
            context = None

        # Formats queried data into digestible output to be printed
        # Checks for special print conditions for select categories that require different output
        if context:
            if category == "population":
                tmp = []
                for i in range(len(output)):
                    response = f"{output[i][5]} = {output[i][2]:,}"
                    tmp.append(response)
                print(context + "\n".join(tmp))
                print("\n")
            elif category == "num_counties":
                tmp = []
                for i in range(len(output)):
                    response = f"{output[i][5]} = {output[i][6]}"
                    tmp.append(response)
                print(context + "\n".join(tmp))
                print("\n")
            elif category == "state":
                print(f"Info for: {output[0][5]}")
                print(f"Region: {output[0][4]}")
                print(f"Capital: {output[0][0]}")
                print(f"Governor: {output[0][3]}")
                print(f"Population: {output[0][2]:,}")
                print(f"Number of Counties: {output[0][6]}")
                # Check to see if a state has the optional state_bird or popular_food fields
                checking = True
                while checking:
                    foods = ["Clam Chowder", "Buckeye Candies"]
                    birds = ["Yellowhammer", "Willow Ptarmigan", "Cactus Wren", "California Quail", "Blue Hen Chicken", "Brown Thrasher", "Western Meadowlark", "Northern Cardinal", "Black-capped Chickadee", "Northern Mockingbird", "Mountain Bluebird", "Rhode Island Red", "Hermit Thrush"]
                    try:
                        value = output[0][7]
                    except IndexError:
                        pass
                    try:
                        value2 = output[0][8]
                        print(f"Popular Food: {value}")
                        print(f"State Bird: {value2}")
                        break
                    except IndexError:
                        pass
                    if value in foods:
                        print(f"Popular Food: {value}")
                        checking = False
                    elif value in birds:
                        print(f"State Bird: {value}")
                        checking = False
                    else:
                        break
                print("\n")
            else: # Default output statement
                tmp = []
                for i in range(len(output)):
                    tmp.append(output[i][5])
                print(context + "\n".join(tmp))
                print("\n")

    def main(self):
        self.display_welcome_screen()
        exit_program = False
        while not exit_program:
            user_query = input(">>> ").strip()
            self.validate_and_parse_input(user_query)

if __name__ == "__main__":
    engine = StateQueryEngine()
    engine.main()