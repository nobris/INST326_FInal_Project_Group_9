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
        print("\n First, let's run a scan to identify suspicious charges... just a moment...\n")
        
        # Wait 5 seconds before next code block
        time.sleep(3)
        
        # no suspicious charges found
        if suspicious_charges.empty:
            return f"Guess what? Great news! Our scan did not find any potentially unusual charges for your {account} account between {start_date} and {end_date}."
        
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
    def spending_category_frequency(self): # Tyler
        """ This method creates a frequency table to display the frequency/count of each
        spending category throughout the user's transaction history
        
        Args: 
            transactions(df): the dataframe from which the category frequency table will 
            built off of
            
        Returns:
            category_frequency_table(df): dataframe that displays frequency/count of each
            spending category 
        """
        print("\n Now, we will provide a frequency table of spending categories you use the most.")
        df = self.transactions 
        category_frequency = pd.crosstab(index = df['Category'], columns = 'count').sort_values(['count'], ascending = False)
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
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.

        Side Effects:
            Prints a statement showing the user the data they are looking at in
            the terminal.

        Returns:
            dataframe: A datafrane of the top 5 categories the user spends their money on
            from most amount of money spent to least amount spent.
        """
        print("\nHere are your top 5 spending categories and the amounts you spend for each of them:\n")

        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest

        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
        
        df = self.transactions[date_filter]

        df_cat = df[['Category', 'Amount']].groupby('Category', as_index = False).sum().sort_values('Amount', ascending=False).head(amt)
        return df_cat
    def search_transactions(self, desc): # Tristan
        """Displays transactions where the description matches what the user
        inputs in the argument -d.
        
        Args: 
            desc (str): the word(s) to be searched for within the transactions
            file

        Side Effects:
            Prints statements telling the user whether their search found
            results or not.

        Returns:
            A new dataframe sorted by date based on the price range the
            user input.
        """
        df = self.transactions
        lower_df = df["Description"].str.lower()
        search = df[lower_df.str.contains(desc.lower())]
        if search.empty:
            return("\nYour search resulted in zero matches!")
        else:
            print("\n Here are transactions where descriptions matched what you searched for:\n")
            return search
    def day_of_week_summary(self): # Sophia       
        """Creates dataframe with summary values for the days of the week.
       
       Returns:
           summary_df(df): dataframe containing mean, median, minimum, maximum 
           amount and average amount of transactions used for the days of the week.
        """
        # adds day of the week to data frame
        df = self.transactions
        s1 = df["Date"]
        dow_list = []
        for i in s1:
            day_of_week = i.strftime("%A")
            dow_list.append(day_of_week)
        df["Day of Week"] = pd.Series(dow_list)
        print("\nAdded the day of the week to the data frame to the correseponding date.")
        
        # creates summary data frame
        avg_transactions = []
        means = []
        medians = []
        mins = []
        maxs = []
        days_list = list(set(list(df["Day of Week"])))
        
        for i in days_list:
            #calculates average number of transactions 
            avg_transaction = df[df["Day of Week"]==i].groupby("Date")["Date"].count().mean()    
            avg_transactions.append(avg_transaction)

            #calculates mean amount spent
            mean = df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().mean()
            means.append(mean)
            
            #calculates median amount spent
            median = df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().median()
            medians.append(median)
            
            #finds minimum amount spent
            minimum = df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().min()
            mins.append(minimum)
            
            #finds maximum amount spent
            maximum = df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().max()
            maxs.append(maximum)
        # creates series for each summary value
        s2 = pd.Series(avg_transactions, index = days_list, name = "Avg Transactions")
        s3 = pd.Series(means, index = days_list, name = "Mean")
        s4 = pd.Series(medians, index = days_list, name = "Median")
        s5 = pd.Series(mins, index = days_list, name = "Minimum")
        s6 = pd.Series(maxs, index = days_list, name = "Maximum")
        # concatenates the series
        summary_df = pd.concat([s2,s3,s4,s5,s6], axis = 1)
        print("\nReturns a summary data frame.")
        return summary_df
    
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
    parser.add_argument("-c", "--amt", type = int, default = 5,
                        help ="int amount for top categories")
    parser.add_argument("-d", "--desc", type = str,
                        help ="str specifying description search")

    return parser.parse_args(arglist)

if __name__ == "__main__":
    """ Statement executes code when file is run from cmd line. 
    """
    args = parse_args(sys.argv[1:])
    
    print("\n **Thank you for using Team 9's 'Smart Money' Analyzer for your Mint data!**")
    # Instantiate the class
    print(Bookkeeper(args.mint_csv).suspicious_charges(args.start_date, args.end_date, args.account))
    print(Bookkeeper(args.mint_csv).spending_category_frequency())
    print(Bookkeeper(args.mint_csv).top_categories(args.amt, args.start_date, args.end_date).to_string(index = False))
    if args.desc != None:
        try:
            print(Bookkeeper(args.mint_csv).search_transactions(args.desc).to_string(index = False))
        except:
            print(Bookkeeper(args.mint_csv).search_transactions(args.desc))
    print(Bookkeeper(args.mint_csv).day_of_week_summary())