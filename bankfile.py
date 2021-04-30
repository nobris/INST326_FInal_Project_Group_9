"""Create financial summary information from transaction data in a file.

Read transactions, summarize spending over time, plot spending over time, 
identify suspicious transactions, offer financial advice based on spending,
optionally filter by date range.

"""
from argparse import ArgumentParser
import sys
import pandas as pd
import csv
import matplotlib
import calendar
import datetime
import random
import time

class Bookkeeper: 
    """ This class reads the Mint transactions.csv file for use in following 
        methods/functions.
    
        It includes the following methods:
        suspicous_charges(): flags potentially suspicious charges
        financial_advice(): compares debt to income to offer financial advice
        
        spending_category_frequency(): displays frequency/count of spending by category
        mint_plot(): displays plot of spending each month over time.
        
    
    Attributes:  
        transactions (file): path to file containing user's financial details.
    """
    def __init__(self, transactions): 
        """ Opens the user's financial transaction file, creates and builds a dataframe from it. 
        
            It also converts the Date column in the transaction file into datetime format
        
        Args: 
            transactions (file): The dataframe is made up of of the following columns: 
                date, description, original description, amount, transaction type, 
                category, account name, labels (if any), and notes (if any).
                
        Returns:
            transactions (df): dataframe of the user's financial transactions
            earliest (str): earliest available date from the file
            latest (str): latest available date from the file
        """
        self.transactions = pd.read_csv(transactions)
        # drop empty columns from dataframe
        self.transactions = self.transactions.drop(["Labels", "Notes"], axis = 1)
        
        # change Date column to datetime format
        self.transactions["Date"] = pd.to_datetime(self.transactions["Date"])
        
        # earliest and most recent dates from the user's financial transactions
        self.earliest = str(min(self.transactions["Date"].dt.date))
        self.latest = str(max(self.transactions["Date"].dt.date))

    def suspicious_charges(self, start_date=0, end_date=0, account = None): # Walesia
        """ This method identifies unusual and potentially suspicious transactions.
            
            First, this method filters the df for transactions by the optional
            user specified date range and account name. After calculating the 
            25th and 75th percentiles, it then computes the upper and lower outer
            fences of charges using these formulas: 
            
            lower outer fence: Q1 - 3*IQ
            upper outer fence: Q3 + 3*IQ
            
            Unique debit charges falling outside of the range of either fence
            will be flagged as a suspicious transaction and returned to the user.
        
        Args: 
            mint (df): dataframe of the user's financial transactions
            start_date (str): optional start date in MM-DD-YYYY. Defaults to None.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to None.
            account (str): user 'Account Name' to search. Defaults to None.
            
        Side Effects: 
            Prints a congratulatory message if the scan did not find any potentially 
            suspicious charges. If suspicious charges were found, prints a message
            indicating so.
            
        Returns:
            suspicious_charges (df): Series consisting of the suspicious charges, 
                sorted by date and then amount.
        """
        
        # if user does not specify an Account Name, choose one randomly from the file
        
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest
        
        if account is None:
            account = random.choice(list(self.transactions["Account Name"].unique()))
        
        # create date and account type filters
        account_filter = self.transactions["Account Name"] == account
        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)

        # apply filters, assign to new dataframe variable
        ad_filter = self.transactions[account_filter & date_filter]
        
        # define quartiles based on account charges
        q1 = ad_filter.quantile(q=0.25, axis=0, numeric_only=True, interpolation='linear')
        q3 = ad_filter.quantile(q=0.75, axis=0, numeric_only=True, interpolation='linear')
        # inner quartile range
        iqr = q3-q1

        # outlier formula for suspicious charges
        lower = (q1 - (3*iqr))
        upper = (q3 + (3*iqr))

        # filter for debit charges falling outside of outlier fences.
        suspicious_charges = ad_filter[(ad_filter["Amount"] < float(lower)) |
                                    (ad_filter["Amount"] > float(upper)) &
                                    (ad_filter["Transaction Type"] == "debit")]
        
        # Message to user that this method is running
        print("\n Running a scan to identify suspicious charges... just a moment \n")
        
        # Wait 5 seconds before next code block
        time.sleep(3)
        
        # no suspicious charges found
        if suspicious_charges.empty:
            print("Guess what? Great news! Our scan did not find any potentially unusual charges")
            print(f"for your {account} account between {start_date} and {end_date}.")
        
        # what to do if charges were found
        else:
            print(f"Uh oh! Our scan found these potentially suspicious charges for your {account}")
            print(f"account between {start_date} and {end_date}.")
            print("Check them out here: \n")
            
            # Return list of suspicous charges, dropping duplicate charges, 
            # since frequency would indicate user was likely aware and
            # authorized these purchases.
            return suspicious_charges.drop_duplicates(subset="Description", keep=False, inplace=False)
            
    def financial_advice(transactions, start_date = None, end_date = None): # Walesia
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
    
        Optional arguments for filtering: *Subject to change
    
        - start_date (str or None): the earliest date to include in the methods; 
        If omitted, date will start as far back as possible.
          
        - end_date (str or None): the latest date to include in the methods;
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
    
    parser.add_argument("mint_csv", help ="CSV containing mint transaction data") 
    parser.add_argument("-s", "--start_date", type = str, default = 0,
                        help ="str specifying the start date range; MM-DD-YYYY format")
    parser.add_argument("-e", "--end_date", type = str, default = 0,
                        help ="str specifying the end date range; MM-DD-YYYY format")
    parser.add_argument("-a", "--account", type = str, default = None,
                        help ="str specifying the financial account")

    return parser.parse_args(arglist)

if __name__ == "__main__":
    """ Statement executes code when file is run from cmd line. 
    """
    args = parse_args(sys.argv[1:])
    
    # Instantiate the class
    print(Bookkeeper(args.mint_csv).suspicious_charges(args.start_date, args.end_date, args.account))
    
    
    
    
