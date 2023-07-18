import yfinance as yf
import numpy as np

def calculate_intrinsic_value(stock_symbol):
    stock = yf.Ticker(stock_symbol)

    # Get key information
    info = stock.info

    # Extract relevant fundamental data
    dividend_per_share = info.get('dividendRate', 0)
    earnings_per_share = info.get('trailingEps', 0)
    growth_rate = 0.05  # Assuming a 5% growth rate

    # Calculate intrinsic value using discounted cash flow (DCF) model
    intrinsic_value = (dividend_per_share * (1 + growth_rate)) / (info.get('costOfRevenue', 0) - growth_rate)

    return intrinsic_value


def calculate_price_to_earnings_ratio(stock_symbol):
    stock = yf.Ticker(stock_symbol)

    # Get key information
    info = stock.info

    # Extract relevant fundamental data
    price_per_share = info.get('regularMarketPrice', 0)
    earnings_per_share = info.get('trailingEps', 0)

    # Calculate price-to-earnings (P/E) ratio
    if earnings_per_share != 0:
        pe_ratio = price_per_share / earnings_per_share
    else:
        pe_ratio = np.nan

    return pe_ratio


def calculate_price_to_book_ratio(stock_symbol):
    stock = yf.Ticker(stock_symbol)

    # Get key information
    info = stock.info

    # Extract relevant fundamental data
    price_per_share = info.get('regularMarketPrice', 0)
    book_value_per_share = info.get('bookValue', 0)

    # Calculate price-to-book (P/B) ratio
    if book_value_per_share != 0:
        pb_ratio = price_per_share / book_value_per_share
    else:
        pb_ratio = np.nan

    return pb_ratio


def calculate_dividend_yield(stock_symbol):
    stock = yf.Ticker(stock_symbol)

    # Get key information
    info = stock.info

    # Extract relevant fundamental data
    dividend_per_share = info.get('dividendRate', 0)
    price_per_share = info.get('regularMarketPrice', 0)

    # Calculate dividend yield
    if price_per_share != 0:
        dividend_yield = dividend_per_share / price_per_share
    else:
        dividend_yield = np.nan

    return dividend_yield


def get_fundamentals(stock_symbol):
    intrinsic_value = calculate_intrinsic_value(stock_symbol)
    pe_ratio = calculate_price_to_earnings_ratio(stock_symbol)
    pb_ratio = calculate_price_to_book_ratio(stock_symbol)
    dividend_yield = calculate_dividend_yield(stock_symbol)

    fundamentals = {
        'Intrinsic Value': intrinsic_value,
        'Price-to-Earnings Ratio': pe_ratio,
        'Price-to-Book Ratio': pb_ratio,
        'Dividend Yield': dividend_yield
    }

    return fundamentals
