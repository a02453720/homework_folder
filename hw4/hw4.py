file = open("ubuntu/homework_folder/hw4/TSLA.txt")
lines = file.readlines()
prices = [float(line) for line in lines]

total_profit = 0
first_buy = None
buy_prices = []  # List to keep track of all buy prices

for i in range(5, len(prices)):
    # Establish window and create average price
    avg_price = sum(prices[i-5:i]) / 5
    current_price = prices[i]

    # Test for buy signals
    if current_price < avg_price * 0.98:
        buy_prices.append(current_price)  # Add to list of buys
        if first_buy is None:
            first_buy = current_price  # Store the first buy
        print(f"buying at: {current_price}")

    # Test for sell signals
    elif buy_prices and current_price > avg_price * 1.02:
        sell_price = current_price
        trade_profit = 0

        # Sell all shares bought so far
        while buy_prices:
            buy_price = buy_prices.pop(0)  # Remove the oldest buy
            trade_profit += sell_price - buy_price
            print(f"selling at: {sell_price}")
            print(f"trade profit: {round(sell_price - buy_price, 2)}")

        total_profit += trade_profit  # Add to total profit
    else:
        continue

# Sell any remaining shares at the last price
if buy_prices:
    last_price = prices[-1]
    trade_profit = 0

    # Sell remaining shares
    while buy_prices:
        buy_price = buy_prices.pop(0)
        trade_profit += last_price - buy_price
        print(f"selling remaining stock at: {last_price}")
        print(f"trade profit: {last_price - buy_price, 2}")

    total_profit += trade_profit  # Add remaining profit

# Calculate profit percentage
final_profit_percentage = (total_profit / first_buy) * 100 if first_buy else 0
print("-----------------------")
print(f"Total profit: {round(total_profit, 2)}")
print(f"First buy: {first_buy}")
print(f"% return: {round(final_profit_percentage, 2)}")