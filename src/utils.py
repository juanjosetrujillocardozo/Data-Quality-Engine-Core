"""
Data Quality Engine - Utility Functions
Author: Juan Jose Trujillo Cardozo
Description: Data ingestion and cleaning utilities for enterprise data pipelines.
"""

import csv


def read_csv(file_path):
    """
    Reads a CSV file and returns a list of dictionaries.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        list: List of dictionaries representing each row
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def clean_data(data):
    """
    Cleans and normalizes product data with robust error handling.
    
    Data quality operations:
    - Price normalization (handles $, empty values, malformed strings)
    - Stock level validation (handles 'out of stock', empty, non-numeric)
    - Category standardization (title case normalization)
    - Threshold validation (converts to int, handles missing values)
    
    Args:
        data (list): Raw product data from CSV
        
    Returns:
        list: Cleaned and normalized product data
    """
    cleaned_data = []
    
    for item in data:
        # Price cleaning: remove $, handle empty/invalid
        try:
            price_str = item.get('our_price', '').strip().replace('$', '')
            item['our_price'] = float(price_str) if price_str else None
        except (ValueError, AttributeError):
            item['our_price'] = None
        
        # Stock cleaning: handle 'out of stock' string and invalid values
        stock_value = item.get('current_stock', '').strip()
        if isinstance(stock_value, str) and stock_value.lower() == 'out of stock':
            item['current_stock'] = 0
        elif stock_value:
            try:
                item['current_stock'] = int(stock_value)
            except ValueError:
                item['current_stock'] = 0
        else:
            item['current_stock'] = 0
        
        # Restock threshold cleaning
        try:
            threshold_str = item.get('restock_threshold', '').strip()
            item['restock_threshold'] = int(threshold_str) if threshold_str else 0
        except (ValueError, AttributeError):
            item['restock_threshold'] = 0
        
        # Category normalization (title case)
        category = item.get('category', '').strip()
        item['category'] = category.title() if category else 'Uncategorized'
        
        # Product name cleaning
        item['product_name'] = item.get('product_name', '').strip()
        
        # Only include rows with valid product names
        if item['product_name']:
            cleaned_data.append(item)
    
    return cleaned_data