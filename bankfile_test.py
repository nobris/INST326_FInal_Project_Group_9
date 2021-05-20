"""Tests our bankfile.py code to make sure it operates correctly.
"""
import pytest
import bankfile
import pandas as pd

class TestBookkeeper: 
    
    def __init__(self, transactions): 
        "Mock Bookkeeper object used for testing our functions."
        self.transactions = pd.read_csv(transactions)
        
        # drop empty columns from dataframe
        self.transactions = self.transactions.drop(["Labels", "Notes"], axis = 1)
        
        # change Date column to datetime format
        self.transactions["Date"] = pd.to_datetime(self.transactions["Date"])
        
        # earliest and most recent dates from the user's financial transactions
        self.earliest = str(min(self.transactions["Date"].dt.date))
        self.latest = str(max(self.transactions["Date"].dt.date))
        
# testing suspicious transactions method
def test_suspicious_transactions_no_args():
    """ Checks whether the suspicious transactions method works with no 
    optional arguments.
    """ 
    test = TestBookkeeper("transactions.csv")
    bankfile.Bookkeeper.suspicious_charges(test)
    
def test_suspicious_transactions_one_arg():
    """ Checks whether the suspicious transactions method works with just 
    start date.
    """
    test2 = TestBookkeeper("transactions.csv")
    bankfile.Bookkeeper.suspicious_charges(test2, "04-01-2020", "04-30-2020")
    
def test_suspcious_transactions_two_args():
    """ Checks whether the suspicious transactions method works with start 
    and end dates."
    """
    test3 = TestBookkeeper("transactions.csv")
    bankfile.Bookkeeper.suspicious_charges(test3, "04-01-2020", "04-30-2020")

def test_suspicious_transactions_three_args():
    """Checks whether the suspicous transactions method works with start date, end date
    and optional account name specified. 
    """
    test4 = TestBookkeeper("transactions.csv")
    bankfile.Bookkeeper.suspicious_charges(test4, "04-01-2020", "04-30-2020", "Discover")

def test_search_transactions():
    """Does Bookkeeper.search_transactions return results from the 
    dataframe based on 
    """
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.search_transactions("spotif")
    
    
@pytest.fixture
def test_spending_category_frequency():
    """Testing fixture for spending_category_frequency
    """
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.spending_category_frequency()

def test_day_of_week_summary():
    """Does Bookkeeper.day_of_week_summary return results from the dataframe
    based on 
    """    
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.day_of_week_summary()   
    return r.spending_category_frequency()

def test_category_counts(test_spending_category_frequency):
    """Tests whether or not the counts for each category in the frequency table are
    accurate or not
    """
    df = pd.read_csv("transactions.csv")
    assert test_spending_category_frequency.loc['Shopping', 'count'] == df['Category'].value_counts().Shopping
    assert test_spending_category_frequency.loc['Transfer', 'count'] == df['Category'].value_counts().Transfer
    assert test_spending_category_frequency.loc['Groceries', 'count'] == df['Category'].value_counts().Groceries
    assert test_spending_category_frequency.loc['Restaurants', 'count'] == df['Category'].value_counts().Restaurants
    assert test_spending_category_frequency.loc['Credit Card Payment', 'count'] ==df.loc[df.Category == "Credit Card Payment", 'Category'].count()
    
