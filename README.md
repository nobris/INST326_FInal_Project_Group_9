# INST326_Final_Project_Group_9

Bookkeeper for Mint Transactions

## Our project consists of three main files:

bankfile.py (the main file that is called in terminal to run the program)

banfile_test.py (the test file that uses pytest to verify our methods work)

transactions.csv (the csv file our program parses to organize and display information to the user)

## To run our program from the command line it is called with multiple arguments:

python3 bankfile.py "transactions.csv" [optional arguments]

## Our program has 6 arguments, only one of which is required:

"mint.csv" : the required argument of the filepath name for the csv to be read

-s : "str specifying the start date range; MM-DD-YYYY format"

-e : "str specifying the end date range; MM-DD-YYYY format"

-a : "str specifying the financial account"

-c : "int amount for top categories"

-d : "str specifying description search"

## How to use and interpret the program:

A user would want to use our program to examine their mint transactions. They would download their transactions csv and run our program through the terminal with whatever arguments they choose. When run, the user would interpret the output of our program based on the texts in their terminal.