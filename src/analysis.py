"""
Data Quality Engine - Core Analysis Module
Author: Juan Jose Trujillo Cardozo
Description: Implements business logic validation and market parity analysis.
             Designed for scalable data integrity checks in enterprise environments.
"""

import os
import sys
from utils import read_csv, clean_data


def fetch_market_data(product_name):
    """
    Fetches external market pricing data for validation.
    
    In production environments, this would integrate with:
    - External pricing APIs (e.g., OpenFoodFacts, competitor feeds)
    - Internal data lakes (AWS Athena, Snowflake)
    - Real-time market intelligence platforms
    
    Args:
        product_name (str): Product identifier for market lookup
        
    Returns:
        float: Market reference price, or None if unavailable
    """
    # Simulated market data (replace with API integration in production)
    simulated_market_data = {
        "Organic Coffee Beans (1lb)": 12.99,
        "Premium Green Tea (50 bags)": 8.49,
        "Masala Chai Mix (12oz)": 10.49,
        "Yerba Mate Loose Leaf (1lb)": 13.49,
        "Hot Chocolate Mix (1lb)": 7.99,
        "Earl Grey Tea (100 bags)": 11.49,
        "Espresso Beans (1lb)": 16.49,
        "Chamomile Tea (30 bags)": 6.49,
        "Matcha Green Tea Powder (4oz)": 19.49,
        "Decaf Coffee Beans (1lb)": 15.49,
        "Mint Tea (25 bags)": 7.99,
        "Instant Coffee (8oz)": 11.49,
        "cold brew concentrate": 13.49,
        "Rooibos Tea (40 bags)": 9.99,
    }
    return simulated_market_data.get(product_name, None)


def validate_business_rules(product_data):
    """
    Executes a suite of data quality checks including:
    - Price parity validation vs external market sources
    - Integrity of product pricing models
    - Outlier detection and competitive positioning
    
    This function represents the core business logic validation layer,
    similar to banking-grade rule engines used in financial data ecosystems.
    
    Args:
        product_data (list): List of product dictionaries with pricing info
        
    Returns:
        list: Actionable insights with pricing recommendations
    """
    insights = []
    total_products = len(product_data)
    overpriced_count = 0
    underpriced_count = 0
    competitive_count = 0
    no_data_count = 0
    invalid_price_count = 0
    
    for product in product_data:
        product_name = product['product_name']
        our_price = product['our_price']
        
        # Handle missing/invalid price data
        if our_price is None:
            invalid_price_count += 1
            insights.append(
                f"🚨 **{product_name}**: Invalid or missing price data. Data quality issue detected."
            )
            continue
        
        market_price = fetch_market_data(product_name)
        
        if market_price:
            price_diff = our_price - market_price
            
            if price_diff > 0.01:  # Tolerance for floating point comparison
                overpriced_count += 1
                insights.append(
                    f"⚠️ **{product_name}** is overpriced by ${price_diff:.2f}. "
                    f"Recommended action: Reduce price to ${market_price:.2f} for market competitiveness."
                )
            elif price_diff < -0.01:
                underpriced_count += 1
                insights.append(
                    f"💡 **{product_name}** is underpriced by ${abs(price_diff):.2f}. "
                    f"Opportunity to increase margin to ${market_price:.2f}."
                )
            else:
                competitive_count += 1
                insights.append(
                    f"✅ **{product_name}** is priced competitively at ${our_price:.2f}."
                )
        else:
            no_data_count += 1
            insights.append(
                f"❓ **{product_name}**: No market data available. Manual review required."
            )
    
    # Generate summary statistics
    summary = [
        "## Executive Summary",
        f"- **Total Products Analyzed:** {total_products}",
        f"- **Overpriced Products:** {overpriced_count} ({overpriced_count/total_products*100:.1f}%)",
        f"- **Underpriced Products:** {underpriced_count} ({underpriced_count/total_products*100:.1f}%)",
        f"- **Competitively Priced:** {competitive_count} ({competitive_count/total_products*100:.1f}%)",
        f"- **Missing Market Data:** {no_data_count}",
        f"- **Invalid Price Data:** {invalid_price_count}",
        "\n---\n",
        "## Detailed Analysis\n"
    ]
    
    return summary + insights


def main(csv_path):
    """
    Main execution pipeline for the Data Quality Engine.
    
    Pipeline stages:
    1. Data ingestion from CSV source
    2. Data cleaning and normalization
    3. Business rule validation
    4. Report generation with actionable insights
    """
    print("🚀 Starting Data Quality Engine...")
    print("=" * 60)
    
    # Stage 1: Ingestion
    print(f"📂 Loading data from: {csv_path}")
    try:
        product_data = read_csv(csv_path)
        print(f"   ✓ Loaded {len(product_data)} records")
    except FileNotFoundError:
        print(f"   ✗ Error: File '{csv_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"   ✗ Error reading file: {e}")
        sys.exit(1)
    
    # Stage 2: Cleaning
    print("🧹 Cleaning and normalizing data...")
    clean_product_data = clean_data(product_data)
    print(f"   ✓ Cleaned {len(clean_product_data)} valid records")
    
    # Stage 3: Validation
    print("🔍 Executing business rule validation...")
    insights = validate_business_rules(clean_product_data)
    print(f"   ✓ Generated {len(insights)} insights")
    
    # Stage 4: Reporting
    print("📊 Generating Data Quality Report...")
    with open('report.md', 'w', encoding='utf-8') as report:
        report.write("# Data Quality & Market Analysis Report\n")
        report.write("*Generated by Data Quality Engine Core*\n\n")
        report.write("\n".join(insights))
    
    print("=" * 60)
    print("✅ Report generated successfully! Check 'report.md' for insights.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/analysis.py data/products.csv")
        sys.exit(1)
    else:
        main(sys.argv[1])