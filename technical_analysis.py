def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gains, losses = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    avg_gain = gains.rolling(window).mean()
    avg_loss = abs(losses.rolling(window).mean())
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def calculate_obv(close_prices, volume):
    obv = []
    prev_obv = 0
    for i in range(1, len(close_prices)):
        if close_prices[i] > close_prices[i - 1]:
            current_obv = prev_obv + volume[i]
        elif close_prices[i] < close_prices[i - 1]:
            current_obv = prev_obv - volume[i]
        else:
            current_obv = prev_obv
        obv.append(current_obv)
        prev_obv = current_obv
    return obv
