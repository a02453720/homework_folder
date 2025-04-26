import os
import csv
import json
import requests
import pandas as pd
import time

cryptocurrencies = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano', 'solana']
#sets how many days of historical price data to pull
days = 20
base_url = "https://api.coingecko.com/api/v3"
output_folder = "output"

#checks if ouput folder exists and creates it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def fetch_and_save_data():
    #request to api
    for crypto in cryptocurrencies:
        url = f"{base_url}/coins/{crypto}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        response = requests.get(url, params=params)
        print(f"Fetching data for {crypto} please wait 5 seconds...")

        #request validation
        if response.status_code == 200:
            prices = response.json().get('prices', [])
            if not prices:
                print(f"No data returned for {crypto}. Skipping...")
                continue
            file_path = os.path.join(output_folder, f"{crypto}_prices.csv")
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Price'])
                writer.writerows(prices)
            print(f"Data for {crypto} saved to {file_path}")
        else:
            print(f"Failed to fetch data for {crypto}. Status code: {response.status_code}")
        time.sleep(7) #set to 10 if the last coin is failing 

def analyze_data():
    results = {}
    best_strategies = {}
    global_best = {"crypto": None, "strategy": None, "profit": float("-inf")}

    for crypto in cryptocurrencies:
        file_path = os.path.join(output_folder, f"{crypto}_prices.csv")
        if not os.path.exists(file_path):
            print(f"No data for {crypto}. Skipping...")
            continue

        df = pd.read_csv(file_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

        strategy_profits = {'Mean Reversion': 0, 'SMA': 0, 'Bollinger Bands': 0}

        #start at five so theres a rolling window of 5
        for i in range(4, len(df)):
            rolling_window = df.loc[i-4:i, 'Price']
            sma = rolling_window.mean()
            #adjust sma to bollinger bands
            bb_upper = sma * 1.05
            bb_lower = sma * 0.95
            mean_reversion = sma

            open_price = df.loc[i - 1, 'Price']
            close_price = df.loc[i, 'Price']


            #Mean reversion strategy
            if close_price <= mean_reversion * 0.98:
                strategy_profits['Mean Reversion'] += close_price - open_price
            elif close_price >= mean_reversion * 1.02:
                strategy_profits['Mean Reversion'] += open_price - close_price

            #Simple moving average strat
            if close_price > sma:
                strategy_profits['SMA'] += open_price - close_price
            elif close_price < sma:
                strategy_profits['SMA'] += close_price - open_price

            #Bollinger strategy
            if close_price > bb_upper:
                strategy_profits['Bollinger Bands'] += open_price - close_price
            elif close_price < bb_lower:
                strategy_profits['Bollinger Bands'] += close_price - open_price

        # Find the best strategy for the current cryptocurrency
        best_strategy = max(strategy_profits, key=strategy_profits.get)
        best_profit = strategy_profits[best_strategy]
        best_strategies[crypto] = {'strategy': best_strategy, 'profit': best_profit}
        
        #find best strategy out of all strategies
        if best_profit > global_best["profit"]:
         global_best = {"crypto": crypto, "strategy": best_strategy, "profit": best_profit}


        #add results for this coin to global results dictionary
        results[crypto] = {'strategies': strategy_profits, 'best_strategy': best_strategy, 'profit': best_profit}

    results['best_strategy'] = global_best

    return results

def save_results(results):
    json_path = os.path.join(output_folder, 'results.json')
    with open(json_path, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Results saved to {json_path}")


fetch_and_save_data()
results = analyze_data()
save_results(results)