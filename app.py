from flask import Flask, render_template, request, send_from_directory
import yfinance as yf
import matplotlib.pyplot as plt
import os

CHARTS_FOLDER = 'charts'  # Folder name for storing chart files
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['stock']
        time_frame = request.form['time_frame']
        display_sma = 'sma' in request.form.getlist('chart')
        display_rsi = 'rsi' in request.form.getlist('chart')
        display_obv = 'obv' in request.form.getlist('chart')

        stock = yf.Ticker(stock_symbol)

        # Fetch stock data
        data = stock.history(period=time_frame)
        close_prices = data['Close']
        volume = data['Volume']

        # Delete previously generated chart files
        delete_chart_files()

        # Generate charts
        if display_sma:
            sma_period = 50
            sma_50 = close_prices.rolling(window=sma_period).mean()
            generate_sma_chart(close_prices, sma_50, stock_symbol)

        if display_rsi:
            rsi_period = 14
            rsi_14 = calculate_rsi(close_prices, rsi_period)
            generate_rsi_chart(close_prices, rsi_14, stock_symbol)

        if display_obv:
            obv = calculate_obv(close_prices, volume)
            generate_obv_chart(data.index[1:], obv, stock_symbol)

        return render_template('index.html', stock=stock_symbol, display_sma=display_sma, display_rsi=display_rsi, display_obv=display_obv)

    return render_template('index.html')

@app.route('/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(os.path.join(app.root_path, CHARTS_FOLDER), filename)

def delete_chart_files():
    directory = os.path.join(app.root_path, CHARTS_FOLDER)
    for file in os.listdir(directory):
        if file.endswith(".png"):
            os.remove(os.path.join(directory, file))

def generate_sma_chart(close_prices, sma, stock_symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(close_prices, label='Close')
    plt.plot(sma, label='SMA 50')
    plt.legend()
    plt.title('Stock Analysis - Close Prices and SMA 50')
    plt.xlabel('Date')
    plt.ylabel('Price')
    close_sma_path = f'{stock_symbol}_close_sma.png'
    plt.savefig(os.path.join(app.root_path, CHARTS_FOLDER, close_sma_path))

def generate_rsi_chart(close_prices, rsi, stock_symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(rsi, label='RSI')
    plt.axhline(y=70, color='r', linestyle='--')
    plt.axhline(y=30, color='g', linestyle='--')
    plt.legend()
    plt.title('Stock Analysis - RSI')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    rsi_path = f'{stock_symbol}_rsi.png'
    plt.savefig(os.path.join(app.root_path, CHARTS_FOLDER, rsi_path))

def generate_obv_chart(x, obv, stock_symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(x, obv, color='blue', linewidth=1)
    # Fill positive and negative areas
    for i in range(1, len(x)):
        if obv[i] >= 0:
            plt.fill_between([x[i - 1], x[i]], [0, 0], [obv[i - 1], obv[i]], color='green', alpha=0.5)
        else:
            plt.fill_between([x[i - 1], x[i]], [0, 0], [obv[i - 1], obv[i]], color='red', alpha=0.5)
    plt.axhline(y=0, color='black', linestyle='--')
    plt.title('Stock Analysis - OBV')
    plt.xlabel('Date')
    plt.ylabel('OBV')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)

    obv_path = f'{stock_symbol}_obv.png'
    plt.savefig(os.path.join(app.root_path, CHARTS_FOLDER, obv_path))


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



if __name__ == '__main__':
    app.run(debug=True)
