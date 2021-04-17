"""Create financial summary information from transaction data in a file.

Read transactions, summarize spending over time, plot spending over time, 
identify suspicious transactions, offer financial advice based on spending,
optionally filter by date range, amount, or category.

Print financial summary to txt file.
"""

import pandas as pd
import csv
import matplotlib
import calendar # if we want to convert month numbers in the .csv file 

class Bookkeeper(): 
    """ This class reads the Mint transactions.csv file for use in following 
    modules/functions.
    
        It includes the following methods:
        suspicous_charges(): method flags suspicous charges
        financial_advice(): method compares debt to income to offer financial advice
        spending_category_frequency(): displays frequency/count of spending by category
        mint_plot(): displays plot of spending each month over time.
    
    Attributes:  
        transactions (file): path to file containing user's financial details.
    """
    def __init__(self, transactions): 
        """ Opens the user's financial transaction file, creates and builds a dataframe from it. 
        
        Args: 
            transactions (file): The dataframe is made up of of the following columns: 
                date, description, original description, amount, transaction type, 
                category, account name, labels (if any), and notes (if any).
                
        Returns:
            mint (df): dataframe of the user's financial transactions
        """
    
    def suspicous_charges(mint): # Walesia
        """ This method identifies suspicious transactions by calculating inner 
            and outer outlier fences of charges using the interquartile range.
            
            First, this method filters the df for transactions within the
            user specified date range. Next, calculate outlier fences. Any
            debit charges falling outside of the range of the outer fences
            will be flagged as a susipicious transaction, filtered in a new
            series and returned to the user.
        
        Args: 
            mint (df): user transaction dataframe
            
        Returns:
            suspicous_charges (df): Series consisting of the suspicious charges, 
                sorted by date and then amount.
        """
    def financial_advice(mint): # Walesia
        """ For the user specified date range (if applied) this method will 
            calculate income vs spending and offer financial advice.
            
        Args: 
            mint (df): user transaction df
        
        Returns: 
            financial_advice (str): general advice statements about user spending. 
            
                If expenses > income, function provides
                some strategies to help save more money.
                
                If expenses < income, and difference is < $300,
                function congratulates the user, letting them 
                know what they could do with the extra money.
        """
    def spending_category_frequency(mint): # Tyler
        """ This method creates a frequency table to display the frequency/count of each
        spending category throughout the user's transaction history
        
        Args: 
            mint(df): the dataframe from which the category frequency table will 
            built off of
            
        Returns:
            category_frequency_table(df): dataframe that displays frequency/count of each
            spending category 
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
    
    
