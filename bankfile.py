"""Create financial summary information from transaction data in a file.

Read transactions, summarize spending over time, plot spending over time, identify suspicious transactions, 
optionally filter by date range, amount, or category.

Print financial summary to txt file.
"""

import pandas as pd
import csv
import matplotlib

class Bookkeeper(): 
    """ This class reads the Mint transactions.csv file for use in following modules/functions.
    
    Attributes: 
        ****(methods go here)***
        transactions (str): path to file containing user's financial transactions.
        suspicous_charges(): method flags suspicous charges
    """
    def __init__(self, mint): 
        """ Opens the user's financial transaction file, creates and builds a dataframe from it. 
        
        Args: 
            mint (file): The dataframe is made up of of the following columns: date, description, original description, amount, 
            transaction type, category, account name, labels (if any), and notes (if any).
        """
    
    def suspicous_charges(mint): # Walesia
        """ This method identifies suspicious transactions by calculating inner and outer outlier fences using the interquartile range.
            For the user specified date range, debit charges falling outside of this range  of the outer fences will be flagged as a 
            suspicous transaction and returned to the user.
        
        Args: 
            mint (str): 
        """
    def spending_category_frequency(mint): # Tyler
        """ This method creates a frequency table to display the frequency/count of each
        spending category throughout the user's transaction history
        
        Args: 
            mint (df): the dataframe from which the category frequency table will 
            built off of
            
        Returns:
            category_frequency_table(df): dataframe that displays frequency/count of each
            spending category 
        """
    def mint_plot(mint): # Tyler
        """Creates a bar plot using MatLab that displays total spending in each 
        month to show spending over time
        
        Args: 
            mint(df): dataframe from which the plot will be created from, will use
            Date and Amount to create plot
            
        Returns:
            month_plot((unsure what datatype this would be)): bar plot that displays
            total spending in each month
        """ 
        
def parse_args(arglist): # Group
    """ This function will parse command-line arguments.
    
    Expect one mandatory argument (a mint file of the user's transactions).
    
    Also allow 3-4 optional arguments for filtering:
        - date_range: date range for filtering
            (defaults to entire historical date range)
            
        - category: (gym, food & dining, transfer, groceries, interest income, gas & fuel, alcohol & bars, veterinary, restaurants,
            kids activities, clothing, income, federal fax, shopping, doctor, fast food, personal care, vacation, pharmacy)
            
        - account name: (discover, choice checking, investor checking, online savings account, etc.)
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
    args = parse_args(sys.argv[1:])
    
