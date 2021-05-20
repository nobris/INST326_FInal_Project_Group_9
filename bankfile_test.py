"""Tests our bankfile.py code to make sure it operates correctly.
"""
import pytest
import bankfile
import pandas as pd

def test_search_transactions():
    """Does Bookkeeper.search_transactions return results from the dataframe
    based on 
    """
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.search_transactions("spotif")

def test_suspicious_transactions():
    """ This test checks whether the suspicious transactions test is searching
    all of the user's available accounts.
    """ 

@pytest.fixture
def test_spending_category_frequency():
    """Testing fixture for spending_category_frequency
    """
    r = bankfile.Bookkeeper("transactions.csv")
    return r.spending_category_frequency()

def test_counts(test_spending_category_frequency):
    """Does spending_category_frequency return the correct category counts?
    """
    df = pd.read_csv("transactions.csv")
    assert test_spending_category_frequency.loc['Shopping', 'count'] == df['Category'].value_counts().Shopping
    assert test_spending_category_frequency.loc['Transfer', 'count'] == df['Category'].value_counts().Transfer
    assert test_spending_category_frequency.loc['Groceries', 'count'] == df['Category'].value_counts().Groceries
    assert test_spending_category_frequency.loc['Restaurants', 'count'] == df['Category'].value_counts().Restaurants
    assert test_spending_category_frequency.loc['Credit Card Payment', 'count'] ==df.loc[df.Category == "Credit Card Payment", 'Category'].count()
    
def test_day_of_week_summary():
    """Does Bookkeeper.day_of_week_summary return results from the dataframe
    based on 
    """    
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.day_of_week_summary()   
    
