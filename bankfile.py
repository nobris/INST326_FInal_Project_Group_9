"""Create financial summary information from transaction data in a file.

Read transactions, summarize spending over time, plot spending over time, 
identify suspicious transactions, offer financial advice based on spending,
optionally filter by date range, amount, or category.

Print financial summary to txt file.
"""

import pandas as pd
import csv
import matplotlib

class Bookkeeper(): 
    """ This class reads the Mint transactions.csv file for use in following 
    modules/functions.
    
    Attributes: 
        ****(methods go here)***
        transactions (str): path to file containing user's financial details.
        suspicous_charges(): method flags suspicous charges
    """
    def __init__(self, mint): 
        """ Opens the user's financial transaction file, creates and builds a dataframe from it. 
        
        Args: 
            mint (file): The dataframe is made up of of the following columns: 
                date, description, original description, amount, transaction type, 
                category, account name, labels (if any), and notes (if any).
        """
    
    def suspicous_charges(mint): # Walesia
        """ This method identifies suspicious transactions by calculating inner 
            and outer outlier fences of charges using the interquartile range.
            For the user specified date range, debit charges falling outside of
            this range  of the outer fences will be flagged as a suspicous 
            transaction and returned to the user.
        
        Args: 
            mint (file): user transaction dataframe
        """
    def financial_advice(mint): # Walesia
        """ For the user specified date range (if applied) this method will calculate 
            income vs spending and offer financial advice to the user.
            
        Args: 
            mint (file): user transaction df
            debts ()
            date_range (optional)
        
        Side effects: 
            Prints statements about user spending. 
            If credit card debt/expenses > income, function prints telling the 
            user they need to save.
            If debt/expenses < income, function prints congratultaing the user, 
            letting them know they might want to start investing the excess.
        """
        
def parse_args(arglist): # Group
    """ This function will parse command-line arguments.
    
    Expect one mandatory argument (a mint file of the user's transactions).
    
    Also allow optional arguments for filtering: *Subject to change
        - date_range: date range for filtering
            (defaults to entire historical date range)
            
        - category: (gym, food & dining, transfer, groceries, interest income, 
            gas & fuel, alcohol & bars, veterinary, restaurants, kids activities, 
            clothing, income, federal fax, shopping, doctor, fast food, personal care, 
            vacation, pharmacy, etc.)
            
        - account name: (discover, choice checking, investor checking, online savings, etc.)
            (defaults to include all categories)
            
        - amount: transactions either above/below threshold or within a certain range. 
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument() ### To be populated at office hours group meeting 4/23/2021 16:00 EST with Professor Bills.
    return parser.parse_args(arglist)

if __name__ == "__main__":
    """ Statement executes code when file is run from cmd line. 
    
        TBD, but thinking we might want to print some statement telling the user a separate file has been written for them,
        and detail what that file will contain.
    """
    args = parse_args(sys.argv[1:])
    
    
