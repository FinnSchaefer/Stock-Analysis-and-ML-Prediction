from flask import Flask, render_template, request, send_from_directory
import yfinance as yf
from charts import delete_chart_files, generate_sma_chart, generate_rsi_chart, generate_obv_chart
from technical_analysis import calculate_rsi, calculate_obv
from writeup import generate_sma_writeup, generate_rsi_writeup, generate_obv_writeup
from fundamentals import get_fundamentals

app = Flask(__name__, static_url_path='/static')
@app.route('/',methods=['GET', 'POST'])
#placeholder home page
def index():
    return render_template('analysis.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        stock_symbol = request.form['stock']
        time_frame = request.form['time_frame'] + 'd'
        display_sma = 'sma' in request.form.getlist('chart')
        display_rsi = 'rsi' in request.form.getlist('chart')
        display_obv = 'obv' in request.form.getlist('chart')
        display_fundamental = 'fundamental' in request.form.getlist('chart')
        
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

        # Generate write-ups
        writeups = {}
        if display_sma:
            writeups['sma'] = generate_sma_writeup(stock_symbol, sma_50)

        if display_rsi:
            writeups['rsi'] = generate_rsi_writeup(stock_symbol, rsi_14)

        if display_obv:
            writeups['obv'] = generate_obv_writeup(stock_symbol, obv)

        # Perform fundamental analysis
        fundamentals = {}
        if display_fundamental:
            fundamentals = get_fundamentals(stock_symbol)

        return render_template('analysis.html', stock=stock_symbol, display_sma=display_sma, display_rsi=display_rsi, display_obv=display_obv, display_fundamental=display_fundamental, time_frame=time_frame, writeups=writeups, fundamentals=fundamentals)

    return render_template('analysis.html')


@app.route('/static/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory('static/charts', filename)


if __name__ == '__main__':
    app.run(debug=False)
