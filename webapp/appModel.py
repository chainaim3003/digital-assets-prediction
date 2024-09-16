from flask import Flask, jsonify, request, render_template
import random
import json

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import xgboost as xgb

from datetime import datetime, timedelta

app = Flask(__name__)

# Get current date and time
current_datetime = datetime.now()
    
# Add 24 hours to current date and time
prediction_expiry_timestamp = current_datetime + timedelta(hours=24)

# Home route to render the front-end HTML
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/model', methods=['GET'])
def callModel():
        
        #df = pd.read_csv('./ETH-PREDICTION-MODEL-DATA-WITH-HOLIDAYS.csv')
        #"C:\SATHYA\ZK\ZK-Montreal\digital-asset-prediction-api"
        #df = pd.read_csv('C:/SATHYA/ZK/ZK-Montreal/digital-asset-prediction-api/ETH-PREDICTION-MODEL-DATA-WITH-HOLIDAYS.csv')
        df = pd.read_csv('../ETH-PREDICTION-MODEL-DATA-WITH-HOLIDAYS.csv')
       
       #df = pd.read_csv('C:/SATHYA/ZK/ZK-Montreal/digital-asset-prediction-api/ETH-PREDICTION-MODEL-DATA-NO-HOLIDAYS.csv')

        y = df['NextDayHigh']

        X = df[['ETHA','FETH','ETHW','CETH',
                 'ETHV','QETH','EZET','ETHE','ETH']]
        
        #print(y)

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=410)


        model = xgb.XGBRegressor(n_estimators=100, random_state=410)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        #predictions

        # Get current date and time
        current_datetime = datetime.now()
    
        # Add 24 hours to current date and time
        prediction_expiry_timestamp = current_datetime + timedelta(hours=24)

        new_data = pd.DataFrame({
                'ETHA': [0],
                'FETH': [1],
                'ETHW': [0],
                'CETH': [0.2],
                'ETHV': [0.5],
                'QETH': [0],
                'EZET': [0],
                'ETHE': [-0.2],
                'ETH': [1.5]
            })

        # Predicting the expenses for the new data
        predicted_ETH_nextdayhigh_price = model.predict(new_data);

        print('res   ZERO  >>>>>>>>>>>>>>>>>>>..',predicted_ETH_nextdayhigh_price[0]);

        modelResult = {
            'model_digital_asset': 'ETH',
            'model_digital_asset_name': 'Ethereum',
            'model_digital_asset_price': float(predicted_ETH_nextdayhigh_price[0]),
            'model_digital_asset_next_24_hour_volume(in B)': 'static vol',
            'model_current_time_stamp': current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'model_prediction_expiry_timestamp': prediction_expiry_timestamp.strftime("%Y-%m-%d %H:%M:%S")
          }
        print('modelResult..',modelResult);
        
        # Optional: Convert the dictionary to a JSON-formatted string
        #json_string = json.dumps(modelResult, indent=4);
        #return jsonify(json_string);

        return modelResult

# Route to generate and return random crypto values based on user input
@app.route('/crypto', methods=['GET'])
def get_crypto_values():
    asset = request.args.get('asset').upper()  # Convert to uppercase for consistency
    
    # Get current date and time
    current_datetime = datetime.now()
    
    # Add 24 hours to current date and time
    prediction_expiry_timestamp = current_datetime + timedelta(hours=24)


    if asset == 'BTC':
        # Generate random float values for Bitcoin
        bitcoin_price = round(random.uniform(50000, 60000), 2)
        bitcoin_volume = round(random.uniform(18, 30), 2)
        crypto_data = {
            'digital_asset': 'BTC',
            'digital_asset_name': 'Bitcoin',
            'digital_asset_price': bitcoin_price,
            'digital_asset_next_24_hour_volume(in B)': bitcoin_volume,
            'current_time_stamp': current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'prediction_expiry_timestamp': prediction_expiry_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify(crypto_data)
    
    elif asset == 'ETH':
        # Generate random float values for Ethereum
        ethereum_price = round(random.uniform(2000, 3000), 2)
        ethereum_volume = round(random.uniform(9, 13), 2)
        crypto_data = {
            'digital_asset': 'ETH',
            'digital_asset_name': 'Ethereum',
            'digital_asset_price': ethereum_price,
            'digital_asset_next_24_hour_volume(in B)': ethereum_volume,
            'current_time_stamp': current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'prediction_expiry_timestamp': prediction_expiry_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify(crypto_data)
    
    else:
        return jsonify({'error': 'Invalid asset! Use BTC or ETH.'}), 400

if __name__ == '__main__':
    app.run(debug=True)



