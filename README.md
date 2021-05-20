# Final Project - Team 9 - INST326 Spring 2021

## Background
Our program returns various financial summaries from transactions listed in a .csv file.

Included methods identify suspicious tranactions, give financial advice, summarize and plot spending over time,
and support user search. 

## About our program
### Provided files

**bankfile.py**: the main file that is called in terminal to run the program.

**bankfile_test.py**: the test file that uses pytest to verify our methods work.

**transactions.csv**: the .csv file of user financial data that our program parses.

### To run our program from the command line it is called with multiple arguments:

```
python3 bankfile.py transactions.csv [optional arguments]
```

if that does not work, try:

```
python3 bankfile.py transactions.csv [optional arguments]
```

### Our program has 6 arguments, only one of which is required:

"transactions.csv" : required argument - filepath name for the csv to be read

*the following are optional arguments*:

**-s**: (str) specifying the start date range; MM-DD-YYYY format

**-e**: (str) specifying the end date range; MM-DD-YYYY format

**-a**: (str( specifying the financial account

**-c**: (int) amount to return for top categories

**-d**: (str) specifying description search

## Authors
Sophia Chen
[@chensophiah](https://github.com/chensophiah)

Tristan Clark
[@nobris](https://github.com/nobris)

Tyler Deaner
[@TylerD01](https://github.com/TylerD01)

Walesia Robinson II
[@lisalynn7](http://github.com/lisalynn7)
