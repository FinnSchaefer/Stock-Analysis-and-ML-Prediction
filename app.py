from flask import Flask, render_template, request, send_from_directory
import yfinance as yf
from charts import delete_chart_files, generate_sma_chart, generate_rsi_chart, generate_obv_chart
from technical_analysis import calculate_rsi, calculate_obv
from writeup import generate_sma_writeup, generate_rsi_writeup, generate_obv_writeup
from fundamentals import get_fundamentals
from model import StockESNModel
import numpy as np

app = Flask(__name__, static_url_path='/static')
@app.route('/',methods=['GET', 'POST'])
#placeholder home page
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
def analysis():
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

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        stock_symbol = request.form['stock']

        stock = yf.Ticker(stock_symbol)
        data = stock.history(period='5d')  # Get recent 5 days data for prediction

        close_prices = data['Close'].values
        input_data = np.expand_dims(close_prices, axis=0)

        model = StockESNModel.load_model(f'{stock_symbol}_model.h5')  # Load your trained model here
        predicted_prices = model.predict(input_data)

        tomorrow_predicted_price = predicted_prices[0][-1]  # Get the prediction for the next day

        model.plot_predicted_vs_actual(predicted_prices[0], close_prices)
        plot_path = model.save_prediction_plot()

        return render_template('prediction.html', stock=stock_symbol, tomorrow_predicted_price=tomorrow_predicted_price, plot_path=plot_path)

    return render_template('prediction.html')

@app.route('/train', methods=['GET','POST'])
def train():
    stock_symbol = request.form['stock']
    stock = yf.Ticker(stock_symbol)
    train_data = stock.history(period='1y')
    train_labels = train_data['Close'].values

    model = StockESNModel(input_size=5, output_size=1)
    model.train(train_data, train_labels, epochs=10)

    # Save the model with the ticker name as part of the filename
    model_filename = f'static/models/{stock_symbol}_model.h5'
    model.save_model(model_filename)

    return "Model trained and saved successfully!"

if __name__ == '__main__':
    app.run(debug=False)
