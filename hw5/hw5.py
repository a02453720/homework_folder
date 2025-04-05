import pandas as pd 
import json


tickers = ["WMT", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC"]

full_path = "/home/ubuntu/homework_folder/hw5/"
extension = '.csv'

def get_prices(ticker):
    data = pd.read_csv(full_path+ticker+extension)
    return data["Close/Last"].str.replace("$", "").astype(float).tolist()

def mean_reversion_strategy(prices, window):
    avg = 0
    shares = 0
    total_profit = 0
    first_buy = True
    for i in range(len(prices)):
        if i < window:
            avg = sum(prices[0:i])/ max(i, 1)
        else:
            avg = sum(prices[i-window:i])/window

        if prices[i] < avg * .98:
            #buy signal
            shares += 1
            total_profit -= prices[i]
            if first_buy:
                first_buy_val = prices[i]
                first_buy = False
        elif prices[i] > avg * 1.02 and shares != 0:
            #sell signal
            total_profit += prices[i]*shares
            shares = 0
        
    if shares != 0:
        total_profit += prices[-1]*shares

    values = {
        'prices': prices,
        'total_profit': total_profit,
        'first_buy_val': first_buy_val,
        'profit_percentage': (total_profit/ first_buy_val) if not first_buy else 0
    }
    return values

def moving_average_strategy(prices, window):
    avg = 0
    shares = 0
    total_profit = 0
    first_buy = True
    for i in range(len(prices)):
        if i < window:
            avg = sum(prices[0:i])/max(i,1)
        else:
            avg = sum(prices[i-window:i])/window

        if prices[i] > avg:
            #buy signal
            shares += 1
            total_profit -= prices[i]
            if first_buy:
                first_buy_val = prices[i]
                first_buy = False
        elif prices[i] < avg and shares != 0:
            #sell signal
            total_profit += prices[i]*shares
            shares = 0
        
    if shares != 0:
        total_profit += prices[-1]*shares

    values = {
        'prices': prices,
        'total_profit': total_profit,
        'first_buy_val': first_buy_val,
        'profit_percentage': (total_profit/ first_buy_val) if not first_buy else 0
    }
    return values


def test_strategies(window):
    mean_data = []
    moving_data = []
    columns = ["Ticker", "Profit", "%", "1st Buy"]
    for t in tickers:
        prices = get_prices(t)
        window = 5
        mean_vals = mean_reversion_strategy(prices, window)
        moving_vals = moving_average_strategy(prices, window)
        with open(f'{t}_mean.json', "w") as file:
            json.dump(mean_vals, file, indent=4)
        with open(f'{t}_moving.json', "w") as file:
            json.dump(moving_vals, file, indent=4)
        mean_data.append([t, mean_vals['total_profit'], mean_vals['profit_percentage'], mean_vals['first_buy_val']])
        moving_data.append([t, moving_vals['total_profit'], moving_vals['profit_percentage'], moving_vals['first_buy_val']])

   
    df = pd.DataFrame(mean_data, columns=columns)
    print("Mean Strategy")
    print(df.to_string(index=False))

    df = pd.DataFrame(moving_data, columns=columns)
    print("Moving Strategy")
    print(df.to_string(index=False))

    

test_strategies(5)

    
