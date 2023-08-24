import tensorflow as tf
from tensorflow_addons.layers import ESN
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os

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

    def predict(self, input_data):
        # Reshape input_data if needed
        if len(input_data.shape) == 1:
            input_data = input_data.reshape(1, -1)

        # Perform prediction
        predictions = self.model.predict(input_data)

        return predictions

    def save_model(self, filename):
        models_folder = os.path.join("static", "models")
        os.makedirs(models_folder, exist_ok=True)
        full_path = os.path.join(models_folder, filename)
        self.model.save(full_path)
        
        
    # Load model from file
    #makes sense for this method to be a class method because 
    #constructing and returning an instance of the class based on the loaded model
    #and not acting on a specific instance of the class
    @classmethod    
    def load_model(cls, filename):
        models_folder = os.path.join("static", "models")
        full_path = os.path.join(models_folder, filename)
        loaded_model = tf.keras.models.load_model(full_path, custom_objects={"ESN": ESN})
        input_size = loaded_model.layers[0].input_shape[-1]
        output_size = loaded_model.layers[-1].output_shape[-1]
        reservoir_size = loaded_model.layers[0].units
        spectral_radius = loaded_model.layers[0].spectral_radius
        esn_model = cls(input_size, output_size, reservoir_size, spectral_radius)
        esn_model.model = loaded_model
        return esn_model
    
    def summary(self):
        return self.model.summary()
    
    def evaluate(self, test_data, test_labels):
        predictions = self.model.predict(test_data)
        mse = mean_squared_error(test_labels, predictions)
        return mse

    def hyperparam_tuning(self, train_data, train_labels, val_data, val_labels, param_grid, epochs=10):
        best_mse = float('inf')
        best_params = None

        for params in param_grid:
            self.reservoir_size = params['reservoir_size']
            self.spectral_radius = params['spectral_radius']

            self.model = self.build_model()
            self.train(train_data, train_labels, epochs=epochs)
            mse = self.evaluate(val_data, val_labels)

            if mse < best_mse:
                best_mse = mse
                best_params = params

        return best_params, best_mse
    
    def custom_loss(self, y_true, y_pred):
        #implement later
        pass

    def train_with_custom_loss(self, train_data, train_labels, epochs=10):
        self.model.compile(optimizer='adam', loss=self.custom_loss)
        self.model.fit(train_data, train_labels, epochs=epochs)
