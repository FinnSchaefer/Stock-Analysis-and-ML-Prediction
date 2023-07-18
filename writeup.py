def generate_sma_writeup(stock_symbol, sma):
    # Calculate the recent SMA value
    recent_sma = sma[-1]

    # Determine the trend based on the recent SMA value
    if recent_sma > 0:
        trend = "upward"
    elif recent_sma < 0:
        trend = "downward"
    else:
        trend = "sideways"

    # Generate the write-up
    writeup = f"SMA analysis for {stock_symbol}:\n"
    writeup += f"The recent SMA value is {recent_sma:.2f}, indicating an {trend} trend.\n"
    # Add more analysis and insights as needed

    return writeup


def generate_rsi_writeup(stock_symbol, rsi):
    # Determine the current RSI value
    current_rsi = rsi[-1]

    # Interpret the RSI value
    if current_rsi > 70:
        interpretation = "overbought"
    elif current_rsi < 30:
        interpretation = "oversold"
    else:
        interpretation = "neutral"

    # Generate the write-up
    writeup = f"RSI analysis for {stock_symbol}:\n"
    writeup += f"The current RSI value is {current_rsi:.2f}, indicating {interpretation} conditions.\n"
    # Add more analysis and insights as needed

    return writeup


def generate_obv_writeup(stock_symbol, obv):
    # Determine the recent OBV trend
    obv_diff = obv[-1] - obv[-2]

    # Interpret the OBV trend
    if obv_diff > 0:
        trend = "upward"
    elif obv_diff < 0:
        trend = "downward"
    else:
        trend = "sideways"

    # Generate the write-up
    writeup = f"OBV analysis for {stock_symbol}:\n"
    writeup += f"The OBV trend is {trend}, indicating buying or selling pressure.\n"
    # Add more analysis and insights as needed

    return writeup