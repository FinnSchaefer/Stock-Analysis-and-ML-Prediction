import os
import matplotlib.pyplot as plt
import pandas as pd

plt.switch_backend('Agg') 
CHARTS_FOLDER = 'static/charts'  # Folder name for storing chart files
directory = os.path.join(os.path.dirname(__file__), CHARTS_FOLDER)

def delete_chart_files():
    for file in os.listdir(directory):
        if file.endswith(".png"):
            os.remove(os.path.join(directory, file))


def generate_sma_chart(close_prices, sma, stock_symbol):
    sma_series = pd.Series(sma, index=close_prices.index)
    plt.figure(figsize=(12, 6))
    plt.plot(close_prices.index.tolist(), close_prices, label='Close')
    plt.plot(sma_series.index.tolist(), sma, label='SMA 50')
    plt.legend()
    plt.title('Stock Analysis - Close Prices and SMA 50')
    plt.xlabel('Date')
    plt.ylabel('Price')
    close_sma_path = f'{stock_symbol}_close_sma.png'
    plt.savefig(os.path.join(directory,close_sma_path))


def generate_rsi_chart(close_prices, rsi, stock_symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(rsi, label='RSI')
    plt.axhline(y=70, color='r', linestyle='-')
    plt.axhline(y=30, color='g', linestyle='-')
    plt.legend()
    plt.title('Stock Analysis - RSI')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    rsi_path = f'{stock_symbol}_rsi.png'
    plt.savefig(os.path.join(directory, rsi_path))


def generate_obv_chart(x, obv, stock_symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(x, obv, color='blue', linewidth=1)
    # Fill positive and negative areas
    for i in range(1, len(x)):
        if obv[i] >= 0:
            plt.fill_between([x[i - 1], x[i]], [0, 0], [obv[i - 1], obv[i]], color='green', alpha=0.5)
        else:
            plt.fill_between([x[i - 1], x[i]], [0, 0], [obv[i - 1], obv[i]], color='red', alpha=0.5)
    plt.axhline(y=0, color='black', linestyle='-')
    plt.title('Stock Analysis - OBV')
    plt.xlabel('Date')
    plt.ylabel('OBV')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)

    obv_path = f'{stock_symbol}_obv.png'
    plt.savefig(os.path.join(directory, obv_path))
