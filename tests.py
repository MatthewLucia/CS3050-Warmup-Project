from query import StateQueryEngine
import pyparsing as pp
import unittest
from unittest.mock import patch
import pytest
import sys

class run_tests(unittest.TestCase):

    passed = 0
    failed = 0

    # test_one tests a valid query
    @patch("builtins.print")
    def test_one(self, mock_print):
        engine = StateQueryEngine()
        print("Test one: testing a correct query")

        try:
            query = "region == northeast"
            print("Input: ", query)
            engine.validate_and_parse_input(query)

            print("test_one PASSED")
            self.passed += 1

        except pp.ParseException as e:
            print("test_one FAILED. Error: ", e)
            self.failed += 1
            mock_print.assert_any_call("Error. Could not parse input.\nType 'help' to see how to properly format a query.")

    #test_two tests a valid compound query
    @patch("builtins.print")
    def test_two(self, mock_print):
        engine = StateQueryEngine()
        print("Test two: testing a correct compound query")

        try:
            query = "region == northeast && population > 250000"
            print("Input: ", query)
            engine.validate_and_parse_input(query)

            print("test_two PASSED")
            self.passed += 1

        except pp.ParseException as e:
            print("test_two FAILED. Error: ", e)
            mock_print.assert_any_call("Error. Could not parse input.\nType 'help' to see how to properly format a query.")

        except Exception as e:
            print("test_two FAILED. Error: ", e)
            self.failed += 1

    # test_three tests an incomplete query
    @patch ("builtins.print")
    def test_three(self, mock_print):
        engine = StateQueryEngine()
        print("test_three: testing an incomplete query")

        try:
            query = "governor == "
            print("Input: ", query)
            engine.validate_and_parse_input(query)
            print("test_three FAILED - Exception not raised") # The reason it fails here is because it should throw an exception. If it does not, then validate_and_parse does not work properly
            self.failed += 1

        except pp.ParseException as e:
            print("test_three PASSED. Exception called: ", e)
            self.passed += 1
            mock_print.assert_any_call("Error. Could not parse input.\nType 'help' to see how to properly format a query.")


    # test_four tests for incorrect use of operators
    @patch ("builtins.print")
    def test_four(self, mock_print):  # REVISIT
        engine = StateQueryEngine()
        print("Test four: testing incorrect operator")
        try:
            query = "population <> 200000 "
            print("Input: ", query)
            engine.validate_and_parse_input(query)
            print("test_four FAILED - Exception not raised")
            self.failed += 1

        except Exception as e:
            print("test_four PASSED. Error: ", e)
            self.passed += 1
            mock_print.assert_any_call("Error. Could not parse input.\nType 'help' to see how to properly format a query.")

    # test_five tests for queries with spelling mistakes.
    @patch("builtins.print")
    def test_five(self, mock_print):
        engine = StateQueryEngine()
        print("test_five: testing spelling mistake")

        try:
            query = "gobernor == phil scott"
            engine.validate_and_parse_input(query)
            print("test_five FAILED - Exception not raised")
            self.failed += 1

        except pp.ParseException as e:
            print("test_five PASSED, Error: ", e)
            self.passed += 1
            mock_print.assert_any_call("Error. Could not parse input.\nType 'help' to see how to properly format a query.")

        except Exception as e:
            # Catching any other unexpected exceptions
            print("test_five FAILED, Unexpected exception: " ,e)
            self.failed += 1

    # test_six tests the "help" function
    def test_six(self):
        engine = StateQueryEngine()
        print("test_six: testing the 'help' function")
        try:
            query = "help"
            engine.validate_and_parse_input(query)
            print("test_six PASSED")
            self.passed += 1

        except Exception as e:
            print("test_six FAILED. Error: ", e)

    # test_seven tests the "exit" function
    def test_seven(self):
        engine = StateQueryEngine()
        print("test_seven: testing the 'exit' function")
        try:
            query = "exit"

            with pytest.raises(SystemExit):
                engine.validate_and_parse_input(query)

            assert engine.validate_and_parse_input(query) == 1

            print("test_seven PASSED")

        except Exception as e:
            print("test_seven FAILED. Error: ", e)


    #test_eight tests for a compound query missing an operator
    @patch ("builtins.print")
    def test_eight(self, mock_print):
        engine = StateQueryEngine()
        print("test_eight: testing an incorrect compound query (missing operator)")

        try:
            query = "region == northeast population > 30000000"
            engine.validate_and_parse_input(query)
            print("test_eight FAILED - Exception not raised")

        except pp.ParseException as e:
                mock_print.assert_any_call("Error. Could not parse input.\nType 'help' to see how to properly format a query.")
                print("test_eight PASSED!")
                self.passed += 1

        except Exception as e:
            print("test_eight FAILED! Error: ", e)
            self.failed += 1

    # test_nine ensures that program does not crash if there is no value returned from the database
    def test_nine(self):
        engine = StateQueryEngine()
        print("test_nine: testing return if there are no results for the value given")

        try:
            query = "president == mama"
            engine.validate_and_parse_input(query)
            print("test_nine PASSED")  # We should handle this gracefully, no results found
            self.passed += 1

        except Exception as e:
            print("test_nine FAILED. Error: ", e)
            self.failed += 1

if __name__ == '__main__':
    tests = run_tests()

    tests.test_one()
    print(' ')

    tests.test_two()
    print(' ')

    tests.test_three()
    print(' ')

    tests.test_four()
    print(' ')

    tests.test_five()
    print(' ')

    tests.test_six()
    print(' ')

    tests.test_seven()
    print(' ')

    tests.test_eight()
    print(' ')

    tests.test_nine()
    print(' ')

    print("Tests passed: ", tests.passed)
    print("Tests failed: ", tests.failed)
