import pandas as pd 
import json
import os


tickers = ["WMT", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC"]

full_path = os.getcwd()+"/hw5/"
extension = '.csv'

def get_prices(ticker):
    #read from csv using pandas
    data = pd.read_csv(full_path+ticker+extension)
    return data["Close/Last"].str.replace("$", "").astype(float).round(2).tolist()


def mean_reversion_strategy(prices, window):
    avg = 0
    shares = 0
    total_profit = 0
    first_buy = True
    
    for i in range(len(prices)):
        #calculate averages
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

    #add leftover shares
    if shares != 0:
        total_profit += prices[-1]*shares
    #output to dictionary
    values = {
        'prices': prices,
        'total_profit': round(total_profit, 2),
        'first_buy_val': first_buy_val,
        'profit_percentage': round((total_profit/ first_buy_val)*100 if not first_buy else 0,2),
    }
    return values

def moving_average_strategy(prices, window):
    avg = 0
    shares = 0
    total_profit = 0
    first_buy = True
    for i in range(len(prices)):
        #calculate average
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

    #add leftover shares
    if shares != 0:
        total_profit += prices[-1]*shares
    #output to dictionary
    values = {
        'prices': prices,
        'total_profit': round(total_profit,2),
        'first_buy_val': first_buy_val,
        'profit_percentage': round((total_profit/ first_buy_val)*100 if not first_buy else 0,2),
    }
    return values


def test_strategies(window):
    mean_data = []
    moving_data = []
    columns = ["Ticker", "Profit", "Profit %", "1st Buy"]
    #run strategy on each ticker
    for t in tickers:
        prices = get_prices(t)
        window = 5

        mean_vals = mean_reversion_strategy(prices, window)
        moving_vals = moving_average_strategy(prices, window)
        #create json file with output from each strategy
        folder_path = full_path+"/json_outputs/"
        #program assumes there is a folder called json_outputs
        with open(f'{folder_path}{t}_mean.json', "w") as file:
            json.dump(mean_vals, file, indent=4)
        with open(f'{folder_path}{t}_moving.json', "w") as file:
            json.dump(moving_vals, file, indent=4)

        #add to output table
        mean_data.append([t, mean_vals['total_profit'], f'{mean_vals['profit_percentage']}%', mean_vals['first_buy_val']])
        moving_data.append([t, moving_vals['total_profit'], f'{moving_vals['profit_percentage']}%', moving_vals['first_buy_val']])

   #create output table for each strategy usign pandas
    df = pd.DataFrame(mean_data, columns=columns)
    print("Mean Strategy")
    print(df.to_string(index=False))

    df = pd.DataFrame(moving_data, columns=columns)
    print("Moving Strategy")
    print(df.to_string(index=False))

    

test_strategies(5)

    
