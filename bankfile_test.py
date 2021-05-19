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
    
def test_spending_category_frequency():
    """Does Bookkeeper.spending_category_frequency return results from the dataframe
    based on 
    """
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.spending_category_frequency()

def test_day_of_week_summary():
    """Does Bookkeeper.day_of_week_summary return results from the dataframe
    based on 
    """    
    r = bankfile.Bookkeeper("transactions.csv")
    r2 = r.day_of_week_summary()   
