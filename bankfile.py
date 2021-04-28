"""Create financial summary information from transaction data in a file.

Read transactions, summarize spending over time, plot spending over time, 
identify suspicious transactions, offer financial advice based on spending,
optionally filter by date range.

Print financial summary to txt file.
"""

import pandas as pd
import csv
import matplotlib
import calendar # if we want to convert month numbers in the .csv file to their name

class Bookkeeper(): 
    """ This class reads the Mint transactions.csv file for use in following 
    modules/functions.
    
        It includes the following methods:
        suspicous_charges(): method flags suspicous charges
        financial_advice(): method compares debt to income to offer financial advice
        spending_category_frequency(): displays frequency/count of spending by category
        mint_plot(): displays plot of spending each month over time.
        
        4/16/21: Not yet sure what the exact format will be for adding filters 
        to our methods,expecting to get more clarity next week.
    
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
    
    def suspicous_charges(mint, start_date=None, end_date=None, account = None): # Walesia
        """ This method identifies suspicious transactions by calculating inner 
            and outer outlier fences of charges using the interquartile range.
            
            First, this method filters the df for transactions within the opt.
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
    def financial_advice(mint, start_date = None, end_date = None): # Walesia
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
    def top_categories(mint): # Tristan
        """Returns the top 5 categories the user spends their money on.
        
        Args:
            mint(df): the dataframe of mint transactions which will calculate
            based on values within.
            
        Returns:
            list: A list of the top 5 categories the user spends their money on
            from most amount of money spent to least amount spent.
        """
    def price_range(mint): # Tristan
        """Shows a list of transaction based on a price range.
        
        Args: the dataframe of mint transactions which will calculate
        based on values within.

        Returns:
            A new dataframe sorted by date based on the price range the
            user input.
        """
  def spendings_category(self, category): # Sophia
       """This method returns the total amount spent for a specific category
      
       Args:
           category(str): the specific category that is calculated from
      
       Returns:
           total(float): the calculated amount spent
       """
       category_filter = df[df["Category"] == category]
       total = category_filter["Amount"].sum()
       return(total)
   def top_subcategory(self, category, amount = 5): # Sophia
       """Finds top transaction type within a specific category
      
       Args:
           category(str): the category that gets used
           amount(int): optional parameter that limits the amount returned
      
       Returns:
           top_transactions(dict): dictionary where key is transaction type and
           value is amount spent limited to the amount       
       """
       
def parse_args(arglist): # Group
    """ This function will parse command-line arguments.
    
    Expect one mandatory argument (a path to a .csv file from Mint
    of the user's transactions).
    
    Also allow optional arguments for filtering: *Subject to change
    
        - startdate (str or None): the earliest date to include in the methods; 
        If omitted, date will start as far back as possible.
          
        - enddate (str or None): the latest date to include in the methods;
        If omitted, the end date will end as recent as possible.
            
        - account (str or None): (discover, choice checking, investor checking, online savings, etc.)
        If omitted, defaults to include all accounts.
        
        - category (str or None): (resturants, credit card payment, pharmacy, gym, grocery, etc.)
        If omitted, defaults to include all available categories 
                
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument() 
    ### To be populated at office hours group meeting 4/23/2021 @ 16:00 EST with Professor Bills.
    return parser.parse_args(arglist)

if __name__ == "__main__":
    """ Statement executes code when file is run from cmd line. 
    
        Output TBD; thinking we might want to print some statement telling the user a separate 
        file has been written for them, and say something about what that file contains.
    """
    args = parse_args(sys.argv[1:])
    
    
