import pandas as pd

# Load the provided Excel file
file_path = 'results_1H copy.xlsx'
df = pd.read_excel(file_path)

# Define constants
initial_capital = 1000
trade_amount = 50
leverage = 20
trade_fee_percentage = 0.005
stoploss_percentage = -0.4

# Initialize variables
capital = initial_capital
results = []
profit_percentages = []
accumulated_volume = 0
volumes = []

# Function to execute trades based on the given conditions
def execute_trades_with_cumulative_capital_and_stoploss(row, capital, accumulated_volume):
    open_price = row['open']
    close_price = row['close']
    high_price = row['high']
    low_price = row['low']
    prediction_high = row['prediction_h']
    prediction_low = row['prediction_l']

    trade_fee = trade_amount * trade_fee_percentage
    trade_profit = []
    # if prediction_low > open_price:
        # Prediction is incorrect, no trade
    #     return capital, trade_profit
    # elif prediction_low < open_price < prediction_high:
    long_trade = (prediction_high - open_price) > (open_price - prediction_low)
    if long_trade:
        # Execute long trade
        take_profit_price = prediction_high
        stoploss_price = open_price * (1 - stoploss_percentage / leverage) 
        if high_price >= take_profit_price:
            profit = trade_amount * (1 - (take_profit_price / open_price)) * leverage - trade_fee
        elif low_price <= stoploss_price:
            profit = trade_amount * (1 - (stoploss_price / open_price)) * leverage - trade_fee
        else:
            profit = trade_amount * (1 - (close_price / open_price)) * leverage - trade_fee
        # Execute short trade
    else:
        take_profit_price = prediction_low
        stoploss_price = open_price * (1 + stoploss_percentage / leverage)
        if low_price <= take_profit_price:
            profit = trade_amount * (1 + (take_profit_price / open_price)) * leverage - trade_fee
        elif high_price >= stoploss_price:
            profit = trade_amount * (1 + (stoploss_price / open_price)) * leverage - trade_fee
        else:
            profit = trade_amount * (1 + (close_price / open_price)) * leverage - trade_fee
            
    trade_profit.append(profit)
    capital += profit

            
    if trade_profit != []:
        volume = trade_amount * leverage * 2
        accumulated_volume += volume

    return capital, trade_profit, accumulated_volume

# Iterate through each row to simulate trading
for index, row in df.iterrows():
    capital, trade_profit_percentage, accumulated_volume = execute_trades_with_cumulative_capital_and_stoploss(row, capital, accumulated_volume)
    results.append(capital)
    profit_percentages.append(trade_profit_percentage)
    volumes.append(accumulated_volume)

# Add the cumulative capital, trade profit percentages, and cumulative volume to the original dataframe
df['cumulative_capital'] = results
df['trade_profit'] = profit_percentages
df['cumulative_volume'] = volumes

# Save the updated dataframe to a new CSV file
final_file_path = 'final_results_1H.csv'
df.to_csv(final_file_path, index=True)
