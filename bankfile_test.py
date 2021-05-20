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

<<<<<<< HEAD
   
def test_day_of_week_summary():
    """Tests the accuracy of the values of the summary values  
    """ 
         
=======
>>>>>>> 9ed0c11917386db8dd1bb2da1f7470e156373a8a
@pytest.fixture
def test_spending_category_frequency():
    """Testing fixture for spending_category_frequency
    """
    r = bankfile.Bookkeeper("transactions.csv")
<<<<<<< HEAD
    r2 = r.spending_category_frequency()
    return r.spending_category_frequency()
    
def test_category_counts(test_spending_category_frequency):
=======
    return r.spending_category_frequency()

def test_counts(test_spending_category_frequency):
<<<<<<< HEAD
>>>>>>> 9ed0c11917386db8dd1bb2da1f7470e156373a8a
    """Tests whether or not the counts for each category in the frequency table are
    accurate or not
=======
    """Does spending_category_frequency return the correct category counts?
>>>>>>> e6403da962f40ba6611c394e83b3daf065cb29ac
    """
    df = pd.read_csv("transactions.csv")
    assert test_spending_category_frequency.loc['Shopping', 'count'] == df['Category'].value_counts().Shopping
    assert test_spending_category_frequency.loc['Transfer', 'count'] == df['Category'].value_counts().Transfer
    assert test_spending_category_frequency.loc['Groceries', 'count'] == df['Category'].value_counts().Groceries
    assert test_spending_category_frequency.loc['Restaurants', 'count'] == df['Category'].value_counts().Restaurants
    assert test_spending_category_frequency.loc['Credit Card Payment', 'count'] ==df.loc[df.Category == "Credit Card Payment", 'Category'].count()
    
<<<<<<< HEAD
=======
def test_day_of_week_summary():
    """Does Bookkeeper.day_of_week_summary return results from the dataframe
    based on 
    """    
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.day_of_week_summary()   
    
>>>>>>> 9ed0c11917386db8dd1bb2da1f7470e156373a8a
