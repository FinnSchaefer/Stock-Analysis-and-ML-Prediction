def generate_sma_writeup(stock_symbol, sma):
    # Calculate the recent SMA value
    recent_sma = sma[-1]

    # Determine the number of data points to consider for trend analysis based on time frame
    num_data_points = min(len(sma), 3) if len(sma) <= 5 else min(len(sma), 5) if len(sma) <= 10 else min(len(sma), 20) if len(sma) <= 30 else min(len(sma), 40) if len(sma) <= 60 else len(sma) // 2

    # Calculate the trend based on the selected number of data points
    trend_sma = "upward" if sma[-1] > sma[-num_data_points] else "downward" if sma[-1] < sma[-num_data_points] else "sideways"

    # Generate the write-up
    writeup = f"SMA analysis for {stock_symbol}:\n"
    writeup += f"The recent SMA value is {recent_sma:.2f}, indicating {trend_sma} trend based on the past {num_data_points} data points.\n"

    # Additional analysis and insights
    if trend_sma == "upward":
        writeup += "The stock price has been showing a consistent upward trend, suggesting positive momentum.\n"
        writeup += "Traders and investors may consider this as a potential buying opportunity.\n"
    elif trend_sma == "downward":
        writeup += "The stock price has been showing a consistent downward trend, suggesting negative momentum.\n"
        writeup += "Traders and investors may approach with caution and consider selling or shorting positions.\n"
    else:
        writeup += "The stock price has been moving in a sideways pattern, indicating a lack of clear direction.\n"
        writeup += "Traders and investors may wait for a breakout or further confirmation before taking any action.\n"

    return writeup


def generate_rsi_writeup(stock_symbol, rsi):
    # Determine the current RSI value
    current_rsi = rsi[-1]

    # Determine the number of data points to consider for trend analysis based on time frame
    num_data_points = min(len(rsi), 3) if len(rsi) <= 5 else min(len(rsi), 5) if len(rsi) <= 10 else min(len(rsi), 20) if len(rsi) <= 30 else min(len(rsi), 40) if len(rsi) <= 60 else len(rsi) // 2

    # Calculate the trend based on the selected number of data points
    trend_rsi = "overbought" if rsi[-1] > 70 else "oversold" if rsi[-1] < 30 else "neutral"

    # Generate the write-up
    writeup = f"RSI analysis for {stock_symbol}:\n"
    writeup += f"The current RSI value is {current_rsi:.2f}, indicating {trend_rsi} conditions based on the past {num_data_points} data points.\n"

    # Additional analysis and insights
    if trend_rsi == "overbought":
        writeup += "The RSI value is in the overbought territory, suggesting the stock may be overvalued.\n"
        writeup += "Traders and investors may consider this as a potential selling opportunity.\n"
    elif trend_rsi == "oversold":
        writeup += "The RSI value is in the oversold territory, suggesting the stock may be undervalued.\n"
        writeup += "Traders and investors may consider this as a potential buying opportunity.\n"
    else:
        writeup += "The RSI value is in the neutral territory, indicating a balanced market sentiment.\n"
        writeup += "Traders and investors may monitor other technical indicators or catalysts for further confirmation.\n"

    return writeup


def generate_obv_writeup(stock_symbol, obv):
    # Determine the recent OBV trend
    obv_diff = obv[-1] - obv[-2]

    # Determine the number of data points to consider for trend analysis based on time frame
    num_data_points = min(len(obv), 3) if len(obv) <= 5 else min(len(obv), 5) if len(obv) <= 10 else min(len(obv), 20) if len(obv) <= 30 else min(len(obv), 40) if len(obv) <= 60 else len(obv) // 2

    # Calculate the trend based on the selected number of data points
    trend_obv = "upward" if obv_diff > 0 else "downward" if obv_diff < 0 else "sideways"

    # Generate the write-up
    writeup = f"OBV analysis for {stock_symbol}:\n"
    writeup += f"The OBV trend is {trend_obv} trend based on the past {num_data_points} data points, indicating buying or selling pressure.\n"

    # Additional analysis and insights
    if trend_obv == "upward":
        writeup += "The OBV line has been showing a consistent increase, suggesting buying pressure is outweighing selling pressure.\n"
        writeup += "Traders and investors may consider this as a positive signal for the stock.\n"
    elif trend_obv == "downward":
        writeup += "The OBV line has been showing a consistent decrease, suggesting selling pressure is outweighing buying pressure.\n"
        writeup += "Traders and investors may approach with caution and monitor for further developments.\n"
    else:
        writeup += "The OBV line has been moving in a sideways pattern, indicating a balance between buying and selling pressure.\n"
        writeup += "Traders and investors may wait for a breakout or additional confirmation before taking any action.\n"

    return writeup
