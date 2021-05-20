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

# testing search transactions method
def test_search_transactions():
    """Does Bookkeeper.search_transactions return results from the dataframe
    based on?
    """
    r = bankfile.Bookkeeper("transactions.csv")

    r2 = r.search_transactions("spotify")
    rows = r2.shape[0]
    for i in r2["Description"]:
        assert i == "Spotify"
    assert rows == 12

    r3 = r.search_transactions("amazon")
    rows2 = r3.shape[0]
    for j in r3["Description"]:
        if "amazon" in j.lower():
            assert True
        else:
            assert False
    assert rows2 == 231

@pytest.fixture   
def test_day_of_week_summary():
    r = bankfile.Bookkeeper("transactions.csv")
    return r.day_of_week_summary()

def test_dows_values(test_day_of_week_summary):
    """Does day_of_week_summary return the correct values for each summary category?
    """
    df = pd.read_csv("transactions.csv")
    df["Day of Week"] = df["Date"].dt.strftime("%A")
    
    assert test_day_of_week_summary.loc['Monday', 'Avg Transactions'] == round(df[df["Day of Week"]=='Monday'].groupby("Date")["Date"].count().mean(),2)
    assert test_day_of_week_summary.loc['Tuesday', 'Mean'] == round(df[df["Day of Week"]=='Tuesday'].groupby("Date")["Amount"].sum().mean(),2)
    assert test_day_of_week_summary.loc['Wednesday', 'Median'] == round(df[df["Day of Week"]=='Wednesday'].groupby("Date")["Amount"].sum().median(),2)
    assert test_day_of_week_summary.loc['Thursday', 'Minimum'] == round(df[df["Day of Week"]=='Thursday'].groupby("Date")["Amount"].sum().min(),2)
    assert test_day_of_week_summary.loc['Friday', 'Maximum'] == round(df[df["Day of Week"]=='Friday'].groupby("Date")["Amount"].sum().max(),2)
    
         
@pytest.fixture
def test_spending_category_frequency():
    """Testing fixture for spending_category_frequency
    """
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.spending_category_frequency()
    return r.spending_category_frequency()
    
def test_category_counts(test_spending_category_frequency):
    """Does spending_category_frequency return the correct value for each category count/frequency?
    """
    df = pd.read_csv("transactions.csv")
    assert test_spending_category_frequency.loc['Shopping', 'count'] == df['Category'].value_counts().Shopping
    assert test_spending_category_frequency.loc['Transfer', 'count'] == df['Category'].value_counts().Transfer
    assert test_spending_category_frequency.loc['Groceries', 'count'] == df['Category'].value_counts().Groceries
    assert test_spending_category_frequency.loc['Restaurants', 'count'] == df['Category'].value_counts().Restaurants
    assert test_spending_category_frequency.loc['Credit Card Payment', 'count'] == df.loc[df.Category == "Credit Card Payment", 'Category'].count()
       
if __name__ == "__main__":
    test_search_transactions()
