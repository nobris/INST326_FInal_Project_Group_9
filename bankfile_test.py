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
    """Does spending_category_frequency return the correct category counts?
    """
    df = pd.read_csv("transactions.csv")
    assert test_spending_category_frequency.loc['Shopping', 'count'] == df['Category'].value_counts().Shopping
    assert test_spending_category_frequency.loc['Transfer', 'count'] == df['Category'].value_counts().Transfer
    assert test_spending_category_frequency.loc['Groceries', 'count'] == df['Category'].value_counts().Groceries
    assert test_spending_category_frequency.loc['Restaurants', 'count'] == df['Category'].value_counts().Restaurants
    assert test_spending_category_frequency.loc['Credit Card Payment', 'count'] ==df.loc[df.Category == "Credit Card Payment", 'Category'].count()
    
