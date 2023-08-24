import tensorflow as tf
from tensorflow_addons.layers import ESN

class StockESNModel:
    def __init__(self, input_size, output_size, reservoir_size=200, spectral_radius=0.9):
        self.input_size = input_size
        self.output_size = output_size
        self.reservoir_size = reservoir_size
        self.spectral_radius = spectral_radius
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            ESN(self.reservoir_size, spectral_radius=self.spectral_radius, return_sequences=True),
            tf.keras.layers.Dense(self.output_size)
        ])
        return model

    def train(self, train_data, train_labels, epochs=10):
        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(train_data, train_labels, epochs=epochs)