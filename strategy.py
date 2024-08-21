import pandas as pd

# Load the provided Excel file
file_path = 'Data_test/results_1H copy.xlsx'
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
    profit = 0
    
    # Determine if the trade is long or short
    long_trade = (prediction_high - open_price) > (open_price - prediction_low)
    
    if long_trade:
        # Long trade logic
        take_profit_price = prediction_high
        stoploss_price = open_price * (1 - stoploss_percentage / leverage)
        
        if high_price >= take_profit_price:
            # Close with take profit
            profit = (take_profit_price - open_price) * leverage * (trade_amount / open_price) - trade_fee
        elif low_price < stoploss_price:
            # Close with stoploss
            profit = (stoploss_price - open_price) * leverage * (trade_amount / open_price) - trade_fee
        else:
            # Close with closing price
            profit = (close_price - open_price) * leverage * (trade_amount / open_price) - trade_fee

    else:
        # Short trade logic
        take_profit_price = prediction_low
        stoploss_price = open_price * (1 + stoploss_percentage / leverage)
        
        if low_price <= take_profit_price:
            # Close with take profit
            profit = (open_price - take_profit_price) * leverage * (trade_amount / open_price) - trade_fee
        elif high_price > stoploss_price:
            # Close with stoploss
            profit = (open_price - stoploss_price) * leverage * (trade_amount / open_price) - trade_fee
        else:
            # Close with closing price
            profit = (open_price - close_price) * leverage * (trade_amount / open_price) - trade_fee

    capital += profit
    accumulated_volume += trade_amount * leverage

    return capital, profit, accumulated_volume

# Iterate through each row to simulate trading
for index, row in df.iterrows():
    capital, trade_profit, accumulated_volume = execute_trades_with_cumulative_capital_and_stoploss(row, capital, accumulated_volume)
    results.append(capital)
    profit_percentages.append(trade_profit)
    volumes.append(accumulated_volume)

# Add the cumulative capital, trade profit percentages, and cumulative volume to the original dataframe
df['cumulative_capital'] = results
df['trade_profit'] = profit_percentages
df['cumulative_volume'] = volumes

# Save the updated dataframe to a new CSV file
final_file_path = 'final_results_1H.csv'
df.to_csv(final_file_path, index=True)
