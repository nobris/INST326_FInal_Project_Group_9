"""Create financial summary information from transaction data in a file.
Read transactions, summarize spending over time, plot spending over time, 
identify suspicious transactions, offer financial advice based on spending,
optionally filter by date range.
"""
from argparse import ArgumentParser
import sys
import pandas as pd
import csv
from matplotlib import pyplot as plt
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
            start_date (str): optional start date in MM-DD-YYYY. Defaults to None.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to None.
            account (str): user 'Account Name' to search. Defaults to None.
            
        Side Effects: 
            Prints a congratulatory message if the scan did not find any potentially 
            suspicious charges. If suspicious charges were found, prints a message
            indicating so, and a list of any suspicious charges for the accounts.
            The method also prints a statement letting the user know the method has
            finished.
            
        """
        # Message to user that this method is running
        print("\n First, let's run a scan to identify suspicious charges... just a moment...\n")
        
        # Wait 2 seconds before next code block
        time.sleep(2)
        
        # if start date and end date aren't specified, scan all the data
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest
        
        # if user does not specify an Account Name, go through all of them
        if account is None:
            accounts = list(self.transactions["Account Name"].unique())
        
            for x in accounts: 
                
                # create date and account type filters
                account_filter = self.transactions["Account Name"] == x
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
                        
                # if no suspicious charges were found
                if suspicious_charges.empty:
                    print(f"Our scan did not find any potentially unusual charges for your {x} account between {start_date} and {end_date}. \n")
                    time.sleep(1)
                
                # what to do if charges were found
                elif not suspicious_charges.empty:
                    print(f"Our scan found these potentially suspicious charges for your {x}")
                    print(f"account between {start_date} and {end_date}. Check them out below: \n")
                    
                    # Return list of suspicous charges, dropping duplicate charges, 
                    # since frequency would indicate user was likely aware and
                    # authorized these purchases.
                    print(suspicious_charges.drop_duplicates(subset="Description", keep=False, inplace=False))
                    print(" ")
                    time.sleep(1)
                        
        # if the user does specify an account, use that one
        elif account is not None:
            user_account = account
            
            # create date and account type filters
            account_filter = self.transactions["Account Name"] == user_account
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
                    
            # if no suspicious charges were found
            if suspicious_charges.empty:
                print(f"Our scan did not find any potentially unusual charges for your {user_account}")
                print(f"account between {start_date} and {end_date}. \n")
                time.sleep(1)
            
            # what to do if charges were found
            else:
                print(f"Our scan found these potentially suspicious charges for your {user_account}")
                print(f"account between {start_date} and {end_date}. Check them out below: \n")
                
                # Print list of suspicous charges, dropping duplicate charges, 
                # since frequency would indicate user was likely aware and
                # authorized these purchases.
                print(suspicious_charges.drop_duplicates(subset="Description", keep=False, inplace=False))
                time.sleep(1)
        
        print("****SUSPICOUS TRANSACTIONS SCAN FINISHED****")
        time.sleep(2)
        
    def financial_advice(self, start_date = None, end_date = None): # Walesia
        """ For the user specified date range (if applied) this method will 
            calculate income vs spending and offer financial advice.
            
            if expenses > income, function provides
            some strategies to help save more money.
            
            if expenses = income, function provides
            some strategies to start budgeting.
            
            if expenses < income, and difference is < $300,
            function congratulates the user, letting them 
            know what they could do with the extra money.
            
        Args: 
            start_date (str): optional start date in MM-DD-YYYY. Defaults to None.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to None.
        
        Side Effects: 
            Prints some general advice statements about user spending. 
            Also prints a statement letting the user know the method has finished.
        """
        # if start date and end date aren't specified, scan all the data
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest
            
        # Message to user that this method is running
        print(" ")
        print(f"Next we'll examine your income vs spending from {start_date} to {end_date}...")
        print(" ")        
        
        # Wait 2 seconds before next code block
        time.sleep(2)
        
        # create date filter
        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
        
        # apply filter, assign to new dataframe variable
        apply_dates = self.transactions[date_filter]        

        # Split-Apply-Combine in single statements to create total debits and credits
        debits = apply_dates[apply_dates["Transaction Type"] == "debit"].groupby("Transaction Type")["Amount"].sum()
        credits = apply_dates[apply_dates["Transaction Type"] == "credit"].groupby("Transaction Type")["Amount"].sum()
        
        income = int(credits)
        
        #subtract debits from credits to get net expenses
        net_total = int(credits) - int(debits)
                
        # if user had a negative net income / spent more than they earned
        if net_total < 0:
            advice = (f" \t Watch out, you spent ${abs(net_total)} more than you earned. \n"
                      "\n"
                      f"\t Check out the rest of the features in our program to figure \n"
                      f"\t out where your money is going and how much you might be able \n"
                      f"\t to cut back on some of your spending."
            )     
            
            print(advice)
            
        # if user spent exactly how much they earned
        elif net_total == 0: 
            advice = (f" \t Our reports show that you spent exactly as much as you earned. \n"
                      "\n"
                      f"\t Writing out a detailed budget is one of the best steps you can take \n"
                      f"\t to help you stay on track and save more money. \n"
            )     
            
            print(advice)
            
        # if user had a net positive income / earned more than they spent
        elif net_total > 0:
            
            advice = (f" \t Keep up the great work! You managed to put away ${abs(net_total)}! \n"
                      "\n"
                      f"\t If you haven't already, make sure sure you build up an emergency fund \n"
                      f"\t for any unexpected expenses. \n"
                      "\n"
                      f"\t After that's taken care of, you may want to consider opening up an \n"
                      f"\t investment vehicle like a Roth IRA or brokerage account."
            )     
            
            print(advice)
            print(" ")
            time.sleep(1)
            
        print("****INCOME VS EXPENSES SCAN FINISHED****")
        time.sleep(2)
            
    def spending_category_frequency(self, start_date=0, end_date=0): # Tyler
        """ This method creates a frequency table to display the frequency/count of each
        spending category throughout the user's transaction history
        
        Args: 
            transactions(df): the dataframe from which the category frequency table will 
            built off of
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
            
        Side effects:
           Prints a category_frequency_table (df): dataframe that displays frequency/count of each
           spending category. 
           Also prints a statement letting the user know when the method has finished.
        """
        
        print("\n")
        print("Now, we will provide a frequency table of spending categories you use the most...")
        time.sleep(2)
        
        if start_date == 0:
            start_date = self.earliest

        if end_date == 0:
            end_date = self.latest

        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)

        df = self.transactions[date_filter]

        category_frequency = pd.crosstab(index = df['Category'], columns = 'count').sort_values(['count'], ascending = False).head(5)
        print(category_frequency)
        print("\n")
        time.sleep(2)
        
        print("****END SPENDING CATEGORY FREQUENCY**** \n")
        time.sleep(2)

    def mint_plot(self,start_date=0,end_date=0): # Tyler
        """Creates a bar plot using MatLab that displays total spending in each 
        month to show spending over time, from lowest spending to highest spending
        
        Args: 
            transactions(df): the dataframe from which the category frequency table will 
            built off of
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
            
        Side Effects:
           Writes to stdout, also prints a statement informing the user that the method has concluded 
           
        Returns:
            month_plot: bar plot that displays the total spending in each month
        """
        print("Here is a bar plot showing the months you have spent the most money,\n")
        print("ordered from the smallest amount to largest amount.")
        print("\n")
        time.sleep(2)
        
        df = self.transactions
        
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest
            
        date_filter = (df["Date"] <= end_date) & (df["Date"] >= start_date)
        df = self.transactions[date_filter]
        month_plot = df.groupby(df['Date'].dt.strftime('%B %Y'))['Amount'].sum().sort_values()
        month_plot.plot.bar(x = 'Date', y = 'Amount')
        
        plt.title("Amount Spent Per Month")
        plt.ylabel("Amount Spent in $")
        plt.show()
        
        month_plot.plot.bar
        
        print("****TOTAL SPENDING PLOT FINISHED**** \n")
        time.sleep(1)
    
    def top_categories(self, amt = 5, start_date = 0, end_date = 0): # Tristan
        """Returns the top 5 categories the user spends their money on and the
        amount related to the category.
        Args:
            amt (int): the argument for the top amount of categories the user
            would like to view.
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
            
        Side Effects:
            Prints df_cat (df) of the top 5 categories the user spends their money on 
            from most amount of money spent to least amount of money spent. 
            
            Also prints a statement showing the user the data they are looking at in
            the terminal, and lets the user know when the method has concluded.
        """
        
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest
            
        print(f"Here are your top 5 spending categories from {start_date} to {end_date}\n"
              f"and the amounts you spent for each of them: \n")
        
        time.sleep(2)
        
        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
        
        df = self.transactions[date_filter]
        df_cat = df[['Category', 'Amount']].groupby('Category', as_index = False).sum().sort_values('Amount', ascending=False).head(amt)
        print(df_cat)
    
        time.sleep(1)
        print("\n****TOP CATEGORIES FINISHED**** \n")
        time.sleep(2)
    
    def search_transactions(self, desc, start_date = 0, end_date = 0): # Tristan
        """Displays transactions where the description matches what the user
        inputs in the argument -d.
        
        Args: 
            desc (str): the word(s) to be searched for within the transactions
            file
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.
        Side Effects:
            Prints statements telling the user whether their search found
            results or not.
        Returns:
            A list of rows containing transactions that match a description
            based on what the user input in their arguments.
        """
        if start_date == 0:
            start_date = self.earliest
            
        if end_date == 0:
            end_date = self.latest
            
        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
        df = self.transactions[date_filter]
        
        lower_df = df["Description"].str.lower()
        
        search = df[lower_df.str.contains(desc.lower())]
        
        if search.empty:
            return("\n Your search resulted in zero matches!")
        
        else:
            print("\n Here are transactions where descriptions matched what you searched for:\n")
            return search
        
    def day_of_week_summary(self, start_date = 0, end_date = 0): # Sophia       
        """Creates dataframe with summary values for the days of the week.
        
       Args:
            start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
            end_date (str): optional end date in MM-DD-YYYY. Defaults to 0.   
            
        Side effects:
            Prints to stdout:
           - summary_df(df): dataframe containing mean, median, minimum, maximum 
           - amount and average amount of transactions used for the days of the week.
           - statement telling the user that the function is finished.
        """
        df = self.transactions       
        if start_date == 0:
            start_date = self.earliest            
        if end_date == 0:
            end_date = self.latest
        date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
        df = self.transactions[date_filter]
                   
        dow_list = []
        for i in df["Date"]:
            dow_list.append(i.strftime("%A"))
        df["Day of Week"] = pd.Series(dow_list)
        
        avg_transactions = []
        means = []
        medians = []
        mins = []
        maxs = []
        days_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        
        for i in days_list:
            avg_transactions.append(round(df[df["Day of Week"]==i].groupby("Date")["Date"].count().mean(),2))
            means.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().mean(),2))
            medians.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().median(),2))
            mins.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().min(),2))
            maxs.append(round(df[df["Day of Week"]==i].groupby("Date")["Amount"].sum().max(),2))

        s2 = pd.Series(avg_transactions, index = days_list, name = "Avg Transactions")
        s3 = pd.Series(means, index = days_list, name = "Mean")
        s4 = pd.Series(medians, index = days_list, name = "Median")
        s5 = pd.Series(mins, index = days_list, name = "Minimum")
        s6 = pd.Series(maxs, index = days_list, name = "Maximum")

        summary_df = pd.concat([s2,s3,s4,s5,s6], axis = 1)
        print("\nHere is your summary information for the days of the week: \n")
        time.sleep(1)
        print(summary_df)
        print("\n")
    
        print("****DAY OF THE WEEK SUMMARY FINISHED****")
    
    def compare_spendings(self, start_date = 0, end_date = 0): # Sophia
       """Compares spendings between most recent weeks, months, and years
       
       Args:
           start_date (str): optional start date in MM-DD-YYYY. Defaults to 0.
           end_date (str): optional end date in MM-DD-YYYY. Defaults to 0. 
       Returns:
           Empty str.     
       Side effects:
           Prints comparison statements.      
       """
       df = self.transactions       
       if start_date == 0:
           start_date = self.earliest            
       if end_date == 0:
           end_date = self.latest
       date_filter = (self.transactions["Date"] <= end_date) & (self.transactions["Date"] >= start_date)
       df = self.transactions[date_filter]
       
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
           print(f"\nHere are how your {itl.index.name.lower()}ly spendings compare: \n")
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
               time.sleep(1)
       return " "            
       
       
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
    
    print("\n **Welcome to Team 9's 'Smart Money' Analyzer for your Mint data!**\n")
    
    # Instantiate the class
    
    Bookkeeper(args.mint_csv).suspicious_charges(args.start_date, args.end_date, args.account)
    Bookkeeper(args.mint_csv).financial_advice(args.start_date, args.end_date)

    Bookkeeper(args.mint_csv).spending_category_frequency(args.start_date, args.end_date)
    
    Bookkeeper(args.mint_csv).mint_plot(args.start_date, args.end_date)
    Bookkeeper(args.mint_csv).top_categories(args.amt, args.start_date, args.end_date)
    
    if args.desc != None:
        try:
            Bookkeeper(args.mint_csv).search_transactions(args.desc, args.start_date, args.end_date).to_string(index = False)
        except:
            Bookkeeper(args.mint_csv).search_transactions(args.desc, args.start_date, args.end_date)
    
    Bookkeeper(args.mint_csv).day_of_week_summary(args.start_date, args.end_date)
    Bookkeeper(args.mint_csv).compare_spendings(args.start_date, args.end_date)

    print("\n **Thank you for using our program!! We hope you found this data analysis useful!**\n")