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
from datetime import timedelta 

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
        print("\n First, let's run a scan to identify suspicious charges... just a moment...\n")
        
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
    def spending_category_frequency(self, start_date=0, end_date=0): # Tyler
        """ This method creates a frequency table to display the frequency/count of each
        spending category throughout the user's transaction history
        
        Args: 
            transactions(df): the dataframe from which the category frequency table will 
            built off of
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
            
        Returns:
            category_frequency_table(df): dataframe that displays frequency/count of each
            spending category 
        """
        print("\n Now, we will provide a frequency table of spending categories you use the most.")
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest

        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
        
        df = self.transactions[date_filter]
         
        category_frequency = pd.crosstab(index = df['Category'], columns = 'count').sort_values(['count'], ascending = False).head(5)
        return category_frequency
        
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
    def top_categories(self, amt = 5, start_date = 0, end_date = 0): # Tristan
        """Returns the top 5 categories the user spends their money on and the
        amount related to the category.
        Args:
            amt (int): the argument for the top amount of categories the user
            would like to view.
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
        Side Effects:
            Prints a statement showing the user the data they are looking at in
            the terminal.
        Returns:
            list: A list of the top 5 categories the user spends their money on
            from most amount of money spent to least amount spent.
        """
        df = self.transactions
        df_cat = df[['Category', 'Amount']].groupby('Category').sum().sort_values('Amount', ascending=False).head(5)
        print("\nHere are your top 5 spending categories and the amounts you spend for each of them:\n")
        print(df_cat)
        
    def price_range(mint): # Tristan
        """Shows a list of transaction based on a price range.
        
        Args: 
            desc (str): the word(s) to be searched for within the transactions
            file
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
        Side Effects:
            Prints statements telling the user whether their search found
            results or not.
        Returns:
            A new dataframe sorted by date based on the price range the
            user input.
        """

    def day_of_week_summary(self): # Sophia       
        """Creates dataframe with summary values for the days of the week.
       
       Returns:
           summary_df(df): dataframe containing mean, median, minimum, maximum 
           amount and average amount of transactions used for the days of the week.
        Side effects:
           Writes to stdout. 
        """
        # adds day of the week to data frame
        df = self.transactions

        dow_list = []
        for i in df["Date"]:
            dow_list.append(i.strftime("%A"))
        df["Day of Week"] = pd.Series(dow_list)
        
        # creates summary data frame
        avg_transactions = []
        means = []
        medians = []
        mins = []
        maxs = []

        days_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        for i in days_list:
            #calculates average amount of transactions   
            avg_transactions.append(round(df[df["Day of Week"]==i].groupby("Date")["Date"].count().mean(),2))

            #calculates mean amount spent
            means.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().mean(),2))
            
            #calculates median amount spent
            medians.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().median(),2))
            
            #finds minimum amount spent
            mins.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().min(),2))
            
            #finds maximum amount spent
            maxs.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().max(),2))
        # creates series for each summary value
        s2 = pd.Series(avg_transactions, index = days_list, name = "Avg Transactions")
        s3 = pd.Series(means, index = days_list, name = "Mean")
        s4 = pd.Series(medians, index = days_list, name = "Median")
        s5 = pd.Series(mins, index = days_list, name = "Minimum")
        s6 = pd.Series(maxs, index = days_list, name = "Maximum")
        # concatenates the series
        summary_df = pd.concat([s2,s3,s4,s5,s6], axis = 1)
        print("\nHere is your summary information for the days of the week:")
        return summary_df
    
    def compare_spendings(self): # Sophia
       """Compares spendings between most recent weeks, months, and years
      
       Side effects:
           Writes to stdout.      
       """
       df = self.transactions
       
       week_list = []
       for i in df["Date"]:
           week_list.append((i - timedelta(i.isocalendar()[2] - 1)).date())
       df["Week"] = pd.Series(week_list)
       
       df["Month"] = df["Date"].dt.strftime("%Y-%m")
       
       df["Year"] = df["Date"].dt.strftime("%Y")

       wk = df.groupby("Week")["Amount"].sum().to_frame()
       mth = df.groupby("Month")["Amount"].sum().to_frame()
       yr = df.groupby("Year")["Amount"].sum().to_frame()
       
       wk["Change"] = wk["Amount"].pct_change()
       mth["Change"] = mth["Amount"].pct_change()
       yr["Change"] = yr["Amount"].pct_change()
       
       for itl in [wk, mth, yr]:
           i = 0
           print(f"\nHere are how your {itl.index.name.lower()}ly spendings compare:")
           for j in reversed(itl.index):
               i += 1
               if itl['Change'][j] > 0:
                   print(
                       f"Your spendings for the {itl.index.name.lower()} of {j} is " 
                       f"{itl['Change'][j] * 100:.2f}% higher than the " 
                       f"{itl.index.name.lower()} of {itl.index[-i-1]} from " 
                       f"${itl['Amount'][-i-1]:.2f} to ${itl['Amount'][j]:.2f}.")
               elif itl['Change'][j] < 0:
                   print(
                       f"Your spendings for the {itl.index.name.lower()} of {j} is "
                       f"{abs(itl['Change'][j]) * 100:.2f}% lower than "
                       f"the {itl.index.name.lower()} of {itl.index[-i-1]} from "
                       f"${itl['Amount'][-i-1]:.2f} to ${itl['Amount'][j]:.2f}.")
               else:
                   print(
                       f"Your spendings for the {itl.index.name.lower()} of {j} is "
                       f"the same as the {itl.index.name.lower()} of {itl.index[-i-1]} " 
                       f"at ${itl['Amount'][j]:.2f}.")
               if i == 5 or i == itl.index.size - 1:
                   break        

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
    
    print("\n **Thank you for using Team 9's 'Smart Money' Analyzer for your Mint data!**")
    
    # Instantiate the class
    
    print(Bookkeeper(args.mint_csv).suspicious_charges(args.start_date, args.end_date, args.account))
    
    print(Bookkeeper(args.mint_csv).spending_category_frequency(args.start_date, args.end_date))
    
    #print(Bookkeeper(args.mint_csv).top_categories(args.amt, args.start_date, args.end_date).to_string(index = False))
    # if args.desc != None:
    #     try:
    #         print(Bookkeeper(args.mint_csv).search_transactions(args.desc, args.start_date, args.end_date).to_string(index = False))
    #     except:
    #         print(Bookkeeper(args.mint_csv).search_transactions(args.desc, args.start_date, args.end_date))
            
    print(Bookkeeper(args.mint_csv).day_of_week_summary())
    
    print(Bookkeeper(args.mint_csv).compare_spendings())
